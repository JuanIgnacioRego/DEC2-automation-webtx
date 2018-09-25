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


# TODO: corregir los casos en los que se reescribe el txData["NROOPERACION"] para evitar el problema de idRepetido
# TODO: antes de correr los test, en el setUp(), agregar QAPI.removeMPOS y .removeCS
# TODO: generar una variable params, que tenga las tuplas


class BaseTest:

    def fillTemplate(self, template, fillingData):

        for attr in [attr for attr in template.__dict__.keys() if attr in fillingData.keys()]:
            getattr(template, attr).fill(fillingData[attr])

    def disableSpecialServices(self, siteId="28464383", paymentMethodId="1"):
        QAPI.unsetTxInTwoSteps(siteId, paymentMethodId)
        QAPI.unsetCS(siteId)

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

    def assertSubtxsByPercentaje(self, sacTxHistory, txData):
        """
        Verify if each subTx from distributed one is right, according to its amount, installments and siteId.
        """

        distributedTxId = txData ["NROOPERACION"]
        distributedTxData = sacTxHistory.getDistributedTx(distributedTxId)
        distributedTx, simpleTxs = distributedTxData[1], distributedTxData[2:]

        amountOfDistributedTx = str(int(txData["MONTO"]) * 10 / 100)
        numberOfSimpleTxs = len(txData["SITEDIST"].split("#"))
        amountOfSimpleTxs = str(((int(txData["MONTO"])) - int(amountOfDistributedTx)) / numberOfSimpleTxs)

        # 1) Assert single tx whose site is father site
        assert_that(distributedTx["NROCOMERCIO"], equal_to_ignoring_case(txData["NROCOMERCIO"]))
        assert_that(distributedTx["MONTO"], equal_to_ignoring_case(amountOfDistributedTx))
        assert_that(distributedTx["CUOTAS"], equal_to_ignoring_case(txData["CUOTAS"]))

        # 2) Assert each simple tx whose sites are subsites
        for i in range(len(simpleTxs)):
            assert_that(simpleTxs[i]["NROCOMERCIO"], equal_to_ignoring_case(txData["SITEDIST"].split("#")[i]))
            assert_that(simpleTxs[i]["MONTO"], equal_to_ignoring_case(amountOfSimpleTxs))
            assert_that(simpleTxs[i]["CUOTAS"], equal_to_ignoring_case(txData["CUOTASDIST"].split("#")[i]))

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
    #layer = LayerSimpleTx #It's necessary to import from Layer import LayerSimpleTx

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
        #(compraSimpleMastercardData, validationMastercardData, True),
        #(Data.compraSimpleNativaVisa, Data.validationNativaVisa, True),
        #(compraSimpleNativaMastercardData, validationNativaMastercardData, True),
    )

    def test_Approved(self, txData, validationData, expectedResult, expectedTxStatus="Autorizada"):
        txResult, satisfactoryTxData = self.runTx(txData, validationData, TemplateCompraSimple)
        assert_that(txResult, expectedResult, "Tx was not approved: it was not possible to reach payment page.")
        self.assertTxInSAC(txData, validationData, expectedTxStatus)
        self.assertTxPPB(txData, expectedTxStatus)

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
    )
    def test_TxInTwoSteps_Approved(self, txData, validationData, expectedResult):
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


    def runTx(self,txData, validationData):
        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           QAPI.getIturanHash(txData, validationData)))
        template = TemplateTxForms(self.driver)
        self.fillTemplate(template, validationData)
        template.SUBMIT.click()

    @params(
        (Data.compraSimpleVisa, Data.validationVisa, True),
    )

    def test_Approved(self, txData, validationData, expectedResult):
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData,validationData)

        templateTxResult = TemplateTxFormsResult(self.driver)
        assert_that(templateTxResult.getTxStatus(),is_(expectedResult), "Tx status (approved/rejected)")
        txId, txAmount, txDate = templateTxResult.getTxResultDetails()
        assert_that(str(int(txAmount.replace("$","").replace(".",""))), txData["MONTO"], "Tx amount")
        assert_that(txDate, time.strftime('%d/%m/%Y'), "Tx date")
        self.assertTxInSAC(txData, validationData)

    @params(
        (Data.compraSimpleVisa, Data.validationVisa_ExpiredCard, False),
    )
    def test_Fail_WrongData(self, txData, validationData, expectedResult):
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData,validationData)

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

        timeToGenerateTimeOutError = datetime.datetime.now()+datetime.timedelta(0,180)
        log.debug("Starting counting time")
        log.wait_until("Waiting for timeout, {} secs".format(lifetime_Forms),
                       lambda: datetime.datetime.now() < timeToGenerateTimeOutError,
                       operator.eq, False, 1)
        log.debug("Finishing counting time")
        template.SUBMIT.click()
        templateTxResult = TemplateTxFormsResult(self.driver)

        #len(self.driver.find_element_by_xpath("h1[text()='El formulario solicitado ha expirado']")

        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")

class AFIP(FormsTx):

    @params(("redbee", "390229680", Data.validationVisa),)
    def test_Payment_Failed_alreadyUsedVep(self, aliasKey, vep, validationData):
        self.runTx(aliasKey, vep, validationData)
        print (self.driver.current_url)
        jsonResult= self.getJsonResult()
        assert_that(jsonResult["status"], equal_to_ignoring_case(u"1"))
        assert_that(jsonResult["response_message"], equal_to_ignoring_case(u"Rechazada"))

    def runTx(self, aliasKey, vep, validationData):

        self.buildForm(aliasKey, vep)
        import Forms
        encryptedVep = Forms.encryptTxId(aliasKey, vep)
        rawForm = Forms.validateAFIP(vep, encryptedVep)
        #self.driver.get("file:///{}/afip_form.html".format(os.getcwd()))
        self.driver.get(rawForm)

        #import time
        #time.sleep(5)
        #template = TemplateAFIPForm(self.driver)
        #self.fillTemplate(template, validationData)
        print (self.driver.current_url)
        #print(self.driver.page_source)
        self.driver.save_screenshot("time1.jpg")
        self.driver.execute_script("document.getElementById('NumeroTarjeta').setAttribute('value', '4509790112684851')")
        self.driver.execute_script("document.getElementById('Nombre').setAttribute('value', 'Hola Pepe')")
        self.driver.execute_script("document.getElementsByName('card_data.card_expiration_month')[0].setAttribute('value', '12')")
        self.driver.execute_script("document.getElementsByName('card_data.card_expiration_year')[0].setAttribute('value', '20')")
        self.driver.execute_script("document.getElementById('cvc').setAttribute('value', '123')")



    def buildForm(self,aliasKey, vep):
        from bs4 import BeautifulSoup
        from io import open
        import Forms
        import os

        encryptedVep = Forms.encryptTxId(aliasKey, vep)
        rawForm = Forms.validateAFIP(vep, encryptedVep)
        htmlParser = BeautifulSoup(rawForm, 'html.parser')
        #htmlParser.form["action"] = "http://{}:{}/payments".format(self.formsBaseURL, self.formsPort)

        htmlFile = open("afip_form.html", "w", encoding="utf-8")
        htmlFile.write(htmlParser.prettify())
        htmlFile.close()

    def getJsonResult(self):
        import urllib2
        import json

        url = urllib2.unquote(self.driver.current_url)
        jsonRaw = url[url.find("result=") + len("result="):]
        jsonResult = json.loads(jsonRaw)

        return jsonResult


#   result={"status":"1","response_message":"Rechazada","vendor_unique_id":"390229684"}