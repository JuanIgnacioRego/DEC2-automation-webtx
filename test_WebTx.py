# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.TemplateCompraSimple import TemplateCompraSimple
from pages.TemplateCompraDistribuida import TemplateCompraDistribuida
from pages.TemplateTxConAgregador import TemplateTxConAgregador
from pages.TemplateTxForms import TemplateTxForms
from pages.TemplateTxFormsResult import TemplateTxFormsResult
from pages.TemplateAFIPForm import TemplateAFIPForm
from pages.Validation import Validation
from pages.SACLogin import SACLogin
from pages.SACInicio import SACInicio
from pages.SAC import SACTxHistory
from pages.ConfirmTx import  ConfirmTx
from pages.RequestBin import RequestBin
import Data
from tools import TraduccionCamposWebTx_SAC, processData
from nose2 import *
from nose2.tools.params import params
import os
from settings import *
import unittest
from hamcrest import *
import QAPI
from Exceptions import *
import poormanslogging as log
import time
import json

# TODO: corregir los casos en los que se reescribe el txData["NROOPERACION"] para evitar el problema de idRepetido
# TODO: antes de correr los test, en el setUp(), agregar QAPI.removeMPOS y .removeCS
# TODO: generar una variable params, que tenga las tuplas
# TODO: manejo de errores: captura de pantalla y dejar abierto webdriver
# TODO: cerrar webdriver al finalizar la ejecución


class BaseTest:

    def fillTemplate(self, template, fillingData):

        for attr in [attr for attr in template.__dict__.keys() if attr in fillingData.keys()]:
            getattr(template, attr).fill(fillingData[attr])

    def disableSpecialServices(self, siteId="28464383", paymentMethodId="1"):
        QAPI.unsetTxInTwoSteps(siteId, paymentMethodId)
        QAPI.unsetCS(siteId)
        QAPI.setURLDinamica(siteId, mode="B")

    def setUp(self):

        self.baseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["baseURL"]
        self.port = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["port"]
        if os.getenv("DRIVER", defaultDriver) == "remote_headless_chrome":
            self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                           desired_capabilities=DesiredCapabilities.CHROME)
        else:
            driverOptions = Options()
            driverOptions.add_argument("--headless")
            self.driver = webdriver.Chrome("/home/juan/Automation/chromedriver")#,chrome_options=driverOptions)
        self.disableSpecialServices()
        #self.driver.implicitly_wait(5)

    def tearDown(self):
        #self.driver.quit()
        pass

    def runTx(self, txData, validationData, txTemplate):
        template = txTemplate(self.driver, self.baseURL, self.port)
        self.fillTemplate(template, txData)
        template.SUBMIT.click()

        validation = Validation(self.driver, txData["MEDIODEPAGO"])
        satisfactoryTxData = {}
        if validation.wasApproved():
            self.fillTemplate(validation, validationData)
            validation.SUBMIT.click()
            if validationData["NROTARJETA"].startswith("5"):
                confirmTx = ConfirmTx(self.driver)
                confirmTx.CONFIRMAR.click()

            #It verifies the tx data that is displayed on screen when it was satisfactory.
            satisfactoryTxData = validation.getSatisfactoryTxData(self.driver, txData["MEDIODEPAGO"],
                                                                  validationData["NROTARJETA"])
            for key in list(set(txData.keys() + validationData.keys()).intersection(satisfactoryTxData.keys())):
                assert_that(txData[key] if txData.has_key(key) else validationData[key],
                            equal_to(satisfactoryTxData[key]))

        return (validation.wasApproved(), satisfactoryTxData)

    def assertTxInSAC(self, txData, validationData, expectedTxStatus="Autorizada", isFatherTx=False, sacTxHistory=None):
        #try:
        txId = txData["NROOPERACION"]

        if not sacTxHistory:
            sacLogin = SACLogin(self.driver)
            sacLogin.login()
            sacInicio = SACInicio(self.driver)
            sacInicio.consulta.click()
            sacTxHistory = SACTxHistory(self.driver)

        sacTxData = sacTxHistory.getTx(txId, isFatherTx)

        assert_that(sacTxHistory.getTxStatus(txId, isFatherTx), equal_to(expectedTxStatus), "Tx status")
        for key in sacTxData:
            assert_that(txData[key] if txData.has_key(key) else validationData[key],
                        equal_to_ignoring_case(sacTxData[key]))

        #except Exception:
        #    raise Warning("There was an error trying to assert tx in SAC. QAPI.checkDB used instead")

    def assertSubtxsByPercentaje(self, sacTxHistory, txData):
        """
        Verify if each subTx from distributed one is right, according to its amount, installments and siteId.
        """
        def calculateAmountByPercentege(site):
            return str(round(int(txData["MONTO"])*percentagesConfiguration[site]/100,2))

        def calculatePercentageByAmount(site):
            return str(round(int(txData["MONTO"]) * percentagesConfiguration[site] / 100, 2))

        distributedTxId = txData ["NROOPERACION"]
        distributedTxData = sacTxHistory.getDistributedTx(distributedTxId)
        distributedTx, simpleTxs = distributedTxData[1], distributedTxData[2:]
        percentagesConfiguration = QAPI.getPercentagesConfiguration(txData["NROCOMERCIO"])
        amountOfDistributedTx = str(int(txData["MONTO"]) * 10 / 100)

        numberOfSimpleTxs = len(txData["SITEDIST"].split("#"))
        #amountOfSimpleTxs = str(((int(txData["MONTO"])) - int(amountOfDistributedTx)) / numberOfSimpleTxs)
        # 1) Assert single tx whose site is father site
        """
        assert_that(distributedTx["NROCOMERCIO"], equal_to_ignoring_case(txData["NROCOMERCIO"]))
        assert_that(distributedTx["MONTO"], equal_to_ignoring_case(amountOfDistributedTx))
        assert_that(distributedTx["CUOTAS"], equal_to_ignoring_case(txData["CUOTAS"]))

        # 2) Assert each simple tx whose sites are subsites
        for i in range(len(simpleTxs)):
            assert_that(simpleTxs[i]["NROCOMERCIO"], equal_to_ignoring_case(txData["SITEDIST"].split("#")[i]))
            assert_that(simpleTxs[i]["MONTO"], equal_to_ignoring_case(calculateAmountByPercentege(simpleTxs[i]["NROCOMERCIO"])))
            assert_that(simpleTxs[i]["CUOTAS"], equal_to_ignoring_case(txData["CUOTASDIST"].split("#")[i]))
        """
        subtxs = {}
        for subtx in distributedTxData[1:]: subtxs[subtx["NROCOMERCIO"]] = subtx

        expectedSubTxAmounts = {}
        for site in percentagesConfiguration:
            expectedSubTxAmounts[site] = calculateAmountByPercentege(site)
        expectedSubTxSites = [site for site in percentagesConfiguration.keys() if percentagesConfiguration[site] >0]

        # La cantidad de ditribuidas
        # Que los montos y sitios de las distribuidas correspondan con el método en cuestión
        for site in subtxs:
            assert_that(float(subtxs[site]["MONTO"]), is_(equal_to(float(expectedSubTxAmounts[site]))),
                        "SubTx {} in site {} - Amount according to percentage configuration".format
                        (subtx["NROOPERACION"], subtx["NROCOMERCIO"]))

        assert_that(subtxs.keys(), is_(equal_to(expectedSubTxSites)),
                    "Expected sites for subtxs")

    def assertSubtxsByAmount(self, sacTxHistory, txData):
        """
        Verify if each subTx from distributed one is right, according to its amount, installments and siteId.
        """

        #TODO: currently, it suposses that you're on SACTxHistory webpage
        distributedTxId = txData["NROOPERACION"]
        subTxs = sacTxHistory.getDistributedTx(distributedTxId)[
                 1:]  # because the first one is the distributedTx, so we take remaining ones

        for i in range(len(subTxs)):
            assert_that(subTxs[i]["NROCOMERCIO"], equal_to_ignoring_case(txData["SITEDIST"].split("#")[i]))
            assert_that(subTxs[i]["MONTO"], equal_to_ignoring_case(txData["IMPDIST"].split("#")[i]))
            assert_that(subTxs[i]["CUOTAS"], equal_to_ignoring_case(txData["CUOTASDIST"].split("#")[i]))

    def assertTxPPB(self, txData, expectedTxStatus):
        txData = processData(txData)

        requestBin = RequestBin(self.driver)
        ppbResult = requestBin.getTx(txData["NROOPERACION"], txData["URLDINAMICA"])

        # Tx status assertion: in PPB, only two status should be informed: "Aprobada" and "Rechazada"
        if expectedTxStatus in ["Autorizada", "Pre autorizada"]:
            assert_that(ppbResult["RESULTADO"], equal_to_ignoring_case("Aprobada"))
        else: #expectedStatus == "Rechazada"
            assert_that(ppbResult["RESULTADO"], equal_to_ignoring_case("Rechazada"))

        for key in [k for k in ppbResult.keys() if k in txData.keys()]:
            assert_that(ppbResult[key], equal_to_ignoring_case(txData[key]), "PPB assertion failed")

class TxSimple(BaseTest, unittest.TestCase):
    """
    Tx Simple.
    """
    #layer = LayerSimpleTx #It's necessary to import from Layer import LayerSimpleTx

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
        #(compraSimpleMastercardData, validationMastercardData, True),
        #(Data.compraSimpleNativaVisa, Data.validationNativaVisa, True),
        #(compraSimpleNativaMastercardData, validationNativaMastercardData, True),
    )

    def test_Approved(self, txData, validationData, expectedResult, expectedTxStatus="Autorizada"):
        """"
        Tx simple, exitosa.
        """
        txResult, satisfactoryTxData = self.runTx(txData, validationData, TemplateCompraSimple)
        assert_that(txResult, expectedResult, "Tx was not approved: it was not possible to reach payment page.")
        self.assertTxInSAC(txData, validationData, expectedTxStatus)
        self.assertTxPPB(txData, expectedTxStatus)

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
    )
    def test_TxInTwoSteps_Approved(self, txData, validationData, expectedResult):
        """Tx simple en dos pasos, exitosa"""
        txData["NROOPERACION"] = "VISA 2PASOS {}".format(str(int(time.time())))
        QAPI.setTxInTwoSteps(txData["NROCOMERCIO"], txData["MEDIODEPAGO"])
        self.test_Approved(txData, validationData, expectedResult, expectedTxStatus="Pre autorizada")
        QAPI.unsetTxInTwoSteps(txData["NROCOMERCIO"], txData["MEDIODEPAGO"])

class TxDistribuida(BaseTest, unittest.TestCase):

    def beforeTest_DistribuidaPorMonto(self, txData):
        QAPI.unsetCS(txData["NROCOMERCIO"])
        QAPI.unsetDistributedTxByPercentage(txData["NROCOMERCIO"])
        QAPI.deleteSubsites(txData["NROCOMERCIO"])
        QAPI.addSubsites(txData["NROCOMERCIO"], txData["SITEDIST"].replace("#", ","))

    def beforeTest_DistribuidaPorPorcentaje(self, txData):
        QAPI.unsetCS(txData["NROCOMERCIO"])
        QAPI.deleteSubsites(txData["NROCOMERCIO"])
        QAPI.addSubsites(txData["NROCOMERCIO"], txData["SITEDIST"].replace("#", ","))
        QAPI.setDistributedTxByPercentage(txData["NROCOMERCIO"])

    @params(
        (Data.compraDistribuidaVisa, Data.validationVisa, True),
    )
    def test_DistribuidaPorPorcentaje_Approved(self, txData, validationData, expectedResult):
        txData["NROOPERACION"]= "VISA " + str(int(time.time()))
        self.beforeTest_DistribuidaPorPorcentaje(txData)
        txResult, satisfactoryTxData = self.runTx(txData, validationData, TemplateCompraDistribuida)
        assert_that (txResult, expectedResult)

        sacLogin = SACLogin(self.driver)
        sacLogin.login()
        sacInicio = SACInicio(self.driver)
        sacInicio.consulta.click()
        sacTxHistory = SACTxHistory(self.driver)

        self.assertTxInSAC(txData, validationData, isFatherTx=True, sacTxHistory=sacTxHistory)
        self.assertSubtxsByPercentaje(sacTxHistory, txData)

    @params(
        (Data.compraDistribuidaVisa, Data.validationVisa, True),
        #(compraDistribuidaMastercardData, validationMastercardData, True),
    )
    def test_DistribuidaPorMonto_Approved(self, txData, validationData, expectedResult):
        self.beforeTest_DistribuidaPorMonto(txData)
        txResult, satisfactoryTxData = self.runTx(txData, validationData, TemplateCompraDistribuida)
        assert_that (txResult, expectedResult)

        sacLogin = SACLogin(self.driver)
        sacLogin.login()
        sacInicio = SACInicio(self.driver)
        sacInicio.consulta.click()
        sacTxHistory = SACTxHistory(self.driver)

        self.assertTxInSAC(txData, validationData, isFatherTx=True, sacTxHistory=sacTxHistory)
        self.assertSubtxsByAmount(sacTxHistory, txData)

class TxSimpleConAgregador(BaseTest, unittest.TestCase):

    @params(
        (Data.compraSimpleConAgregador, Data.validationVisa, True),
    )
    def test_Approved(self, txData, validationData, expectedResult, expectedTxStatus="Autorizada"):
        txData["NROOPERACION"] = "VISA " + str(int(time.time()))
        txResult, satisfactoryTxData = self.runTx(txData, validationData, TemplateTxConAgregador)
        assert_that(txResult, expectedResult)
        self.assertTxInSAC(txData, validationData, expectedTxStatus)

class FormsTx(BaseTest, unittest.TestCase):

    def setUp(self):
        super(FormsTx, self).setUp()
        self.formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
        self.formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]
        import Forms

    def tearDown(self):
        super(FormsTx, self).tearDown()

    def runTx(self, txData, validationData):

        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           QAPI.getIturanHash(txData, validationData)))
        template = TemplateTxForms(self.driver)
        self.fillTemplate(template, validationData)
        template.SUBMIT.click()

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
    )
    def test_Approved(self, txData, validationData, expectedResult):
        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "B")
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData, validationData)

        templateTxResult = TemplateTxFormsResult(self.driver)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")
        txId, txAmount, txDate = templateTxResult.getTxResultDetails()
        assert_that(str(int(txAmount.replace("$", "").replace(".", ""))), txData["MONTO"], "Tx amount")
        assert_that(txDate, time.strftime('%d/%m/%Y'), "Tx date")
        #self.assertTxInSAC(txData, validationData)
        time.sleep(15)
        self.assertTxPPB(txData, "Autorizada")

    @params(
        (Data.compraSimpleVisa, Data.validationVisa_ExpiredCard, False),
    )
    def test_Fail_WrongData(self, txData, validationData, expectedResult):
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData, validationData)

        templateTxResult = TemplateTxFormsResult(self.driver)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult))
        assert_that(calling(self.assertTxInSAC).with_args(txData, validationData), raises(TxNotFoundInSACError))

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, False),
    )
    def test_Fail_TimeoutPaymentForm(self, txData, validationData, expectedResult):
        import datetime
        import operator
        from Data import lifetime_Forms

        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           QAPI.getIturanHash(txData, validationData)))

        log.debug("WebDriver opened the form")
        template = TemplateTxForms(self.driver)
        self.fillTemplate(template, validationData)
        log.debug("WebDriver have just filled the form")

        timeToGenerateTimeOutError = datetime.datetime.now() + datetime.timedelta(0, 180)
        log.debug("Starting counting time")
        log.wait_until("Waiting for timeout, {} secs".format(lifetime_Forms),
                       lambda: datetime.datetime.now() < timeToGenerateTimeOutError,
                       operator.eq, False, 1)
        log.debug("Finishing counting time")
        template.SUBMIT.click()
        templateTxResult = TemplateTxFormsResult(self.driver)

        # len(self.driver.find_element_by_xpath("h1[text()='El formulario solicitado ha expirado']")

        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")

class AFIP(FormsTx):
    import json

    @params(("redbee", Data.txSimpleVisa_AFIP["NROOPERACION"], Data.txSimpleVisa_AFIP, Data.validationVisa_AFIP,
             "Autorizada"))
    def test_Payment_Approved(self, aliasKey, vep, txData, validationData, expectedTxStatus):
        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "A")


        self.runTx(aliasKey, vep, txData, validationData)

        # Verify tx status on current URL
        jsonResponse = self.getJsonResult()
        # Example
        # result = {"status": "0", "response_message": "Autorizada", "vendor_unique_id": "390229100", "processor_unique_id": "6935279", "auth_code": 151824}
        assert_that(jsonResponse.keys(), only_contains("status",
                                                       "response_message",
                                                       "vendor_unique_id",
                                                       "processor_unique_id",
                                                       "auth_code"))
        assert_that(jsonResponse["status"], equal_to_ignoring_case("0"))
        assert_that(jsonResponse["vendor_unique_id"], equal_to_ignoring_case(txData["NROOPERACION"]))
        assert_that(jsonResponse["response_message"], equal_to_ignoring_case("Autorizada"))

        # Verify tx in SAC
        # self.assertTxInSAC(txData, validationData, expectedTxStatus)
        time.sleep(8)

        print (self.assertTxPPB(os.getenv("PPBLINK"), vep, txData, validationData))

    @params(("redbee", Data.txSimpleVisa_AFIP["NROOPERACION"], Data.txSimpleVisa_AFIP, Data.validationVisa_AFIP,
             "Autorizada"))
    def test_Payment_Failed_RepeatedVEP(self, aliasKey, vep, txData, validationData, expectedTxStatus):
        self.runTx(aliasKey, vep, txData, validationData)
        jsonResponse = self.getJsonResult()
        # result = {"status": "1", "response_message": "Rechazada", "vendor_unique_id": "390229684"}
        assert_that(jsonResponse.keys(), only_contains("status",
                                                       "response_message",
                                                       "vendor_unique_id"))
        assert_that(jsonResponse["status"], equal_to_ignoring_case("1"))
        assert_that(jsonResponse["vendor_unique_id"], equal_to_ignoring_case(txData["NROOPERACION"]))
        assert_that(jsonResponse["response_message"], equal_to_ignoring_case("Rechazada"))

    def runTx(self, aliasKey, vep, txData, validationData):
        self.buildForm(aliasKey, vep, txData, validationData)
        self.driver.get("file:///{}/afip_form.html".format(os.getcwd()))

        self.driver.execute_script(
            "document.getElementById('NumeroTarjeta').setAttribute('value', '{}')".format(validationData["NROTARJETA"]))
        self.driver.execute_script(
            "document.getElementById('Nombre').setAttribute('value', '{}')".format(validationData["NOMBREENTARJETA"]))
        self.driver.execute_script(
            "document.getElementsByName('card_data.card_expiration_month')[0].setAttribute('value', '{}')".format(
                validationData["idComboMes"]))
        self.driver.execute_script(
            "document.getElementsByName('card_data.card_expiration_year')[0].setAttribute('value', '{}')".format(
                validationData["idComboAno"]))
        self.driver.execute_script(
            "document.getElementById('cvc').setAttribute('value', '{}')".format(validationData["CODSEGURIDAD"]))
        self.driver.find_element_by_id("boton-pagar").click()

    def buildForm(self, aliasKey, vep, txData, validationData):
        #from bs4 import BeautifulSoup
        from io import open
        import os
        import Forms

        encryptedVep = Forms.encryptTxId(aliasKey, vep)
        rawForm = Forms.validateAFIP(vep, encryptedVep, site=txData["NROCOMERCIO"],
                                     email=validationData["EMAILCLIENTE"])

        rawForm = rawForm.replace('action="payments"',
                                  'action="http://{}:{}/payments"'.format(self.formsBaseURL, self.formsPort))

        htmlFile = open("afip_form.html", "w", encoding="utf-8")
        htmlFile.write(rawForm)
        htmlFile.close()

        """ 
        Lo siguiente es una implementación usando un HTML parser.
        Dado que solo hay un attribute "action", se usó un str.replace() directamente.
        Si el formulario HTML cambia, va a ser necesaria usar la implementación con HTML parser.

        htmlParser = BeautifulSoup(rawForm, 'html.parser')
        htmlParser.form["action"] = "http://{}:{}/payments".format(self.formsBaseURL, self.formsPort)

        htmlFile = open("afip_form.html", "w", encoding="utf-8")
        htmlFile.write(htmlParser.prettify())
        htmlFile.close()
        """

    def getJsonResult(self):
        from urllib2 import unquote


        url = unquote(self.driver.current_url)
        jsonRaw = url[url.find("result=") + len("result="):]
        jsonResult = json.loads(jsonRaw)

        return jsonResult

    def assertTxPPB(self, ppbLink, vep, txData, validationData):
        from Data import vepExample
        requestBin = RequestBin(self.driver)
        ppbData = json.loads (requestBin.getRawBody(vep,ppbLink))


        #Assertion of PPB JSON fields according to PPB JSON model
        #assert_that(ppbData.keys(), only_contains([str(field) for field in vepExample.keys()]))
        #assert_that(ppbData["cp"].keys(), only_contains([str(field) for field in vepExample["cp"].keys()]))

        #Assertion of PPB JSON data according to VEP object
        vepJSONObject = QAPI.getVepJSONObject(vep)
        txInDB = QAPI.getTxFromDB(vep)
        assert_that(ppbData["card_number"], equal_to_ignoring_case(validationData["NROTARJETA"]))



        assert_that(ppbData["number_vep"], equal_to_ignoring_case(vepJSONObject["ticket_payment"]["vep"]["number"]))
        assert_that(ppbData["user_cuit"], equal_to_ignoring_case(vepJSONObject["ticket_payment"]["cuit"]["user"]))


        #cp:
        assert_that(ppbData["cp"]["posting_date"], equal_to_ignoring_case(vepJSONObject["ticket_payment"]["vep"]["creation_date"]))
        assert_that(ppbData["cp"]["transaction_id"], equal_to_ignoring_case(txData["NROOPERACION"]))
        assert_that(ppbData["cp"]["payment_entity"], equal_to_ignoring_case(vepJSONObject["ticket_payment"]["cp"]["payment_entity"]))
        assert_that(ppbData["cp"]["payer_bank"],
                    equal_to_ignoring_case(vepJSONObject["ticket_payment"]["cp"]["payer_bank"]))
        assert_that(ppbData["cp"]["nro_ticket"],
                    equal_to_ignoring_case(str(txInDB["nroticket"])))
        assert_that(ppbData["cp"]["control_code"],
                    equal_to_ignoring_case(str(txInDB["codaut"])))
        assert_that(int(ppbData["cp"]["payment_format"]),
                    equal_to(vepJSONObject["ticket_payment"]["cp"]["payment_format"]))
        #assert_that(ppbData["cp"]["payment_datetime"],
        #            equal_to_ignoring_case(str(txInDB["fecha"])))
        assert_that(ppbData["cp"]["payment_form"],
                    equal_to_ignoring_case(vepJSONObject["ticket_payment"]["vep"]["form"]))
        assert_that(int(ppbData["cp"]["branch_office_type"]),
                    equal_to(vepJSONObject["ticket_payment"]["cp"]["branch_office_type"]))
        assert_that(ppbData["cp"]["taxpayer"],
                    equal_to_ignoring_case(vepJSONObject["ticket_payment"]["cuit"]["taxpayer"]))
        #assert_that(ppbData["cp"]["currency"],
        #            equal_to_ignoring_case(QAPI.getCurrency(vepJSONObject["payment"]["currency"])["idmonedaisoalfa"]))
        #PPB amount field is showed as a string like "30000,00". It's necessary to replace "," per "." to make float cast.
        assert_that(float(ppbData["cp"]["amount"].replace(",",".")),
                    equal_to(float(vepJSONObject["payment"]["amount"])))

