# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.TemplateCompraSimple import TemplateCompraSimple
from pages.TemplateCompraDistribuida import TemplateCompraDistribuida
from pages.TemplateTxConAgregador import TemplateTxConAgregador
from pages.TemplateIturan import TemplateTxForms
from pages.TemplateIturanResult import TemplateTxFormsResult
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
from test_WebTx import BaseTest


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
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData, validationData)

        templateTxResult = TemplateTxFormsResult(self.driver)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")
        txId, txAmount, txDate = templateTxResult.getTxResultDetails()
        assert_that(str(int(txAmount.replace("$", "").replace(".", ""))), txData["MONTO"], "Tx amount")
        assert_that(txDate, time.strftime('%d/%m/%Y'), "Tx date")
        self.assertTxInSAC(txData, validationData)

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



    @params(("redbee", Data.txSimpleVisa_AFIP["NROOPERACION"], Data.txSimpleVisa_AFIP, Data.validationVisa_AFIP,
             "Autorizada"))
    def test_Payment_Approved(self, aliasKey, vep, txData, validationData, expectedTxStatus):
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
        import json

        url = unquote(self.driver.current_url)
        jsonRaw = url[url.find("result=") + len("result="):]
        jsonResult = json.loads(jsonRaw)

        return jsonResultclass FormsTx(BaseTest, unittest.TestCase):
    #TODO: import Forms en setUp(), es necesario ?


    def setUp(self):
        super(FormsTx, self).setUp()
        self.formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
        self.formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]


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

    @params((Data.compraSimpleVisa, Data.validationVisa_Rejected, False),)
    def test_Rejected_RejectedCard(self, txData, validationData, expectedResult):

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
        """
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
        """
        self.driver.find_element_by_id("NumeroTarjeta").send_keys(validationData["NROTARJETA"])
        self.driver.find_element_by_id("Nombre").send_keys(validationData["NOMBREENTARJETA"])
        #Son dos elementos con el mismo id
        self.driver.find_elements_by_id("FechaExpiracion")[0].send_keys(validationData["idComboMes"])
        self.driver.find_elements_by_id("FechaExpiracion")[1].send_keys(validationData["idComboAno"])
        self.driver.find_elements_by_id("cvc")[0].send_keys(validationData["CODSEGURIDAD"])
        self.driver.find_elements_by_id("cvc")[0].submit()


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

class SuperForms(FormsTx):

    def setUp(self):
        super(SuperForms, self).setUp()

    def tearDown(self):
        super(SuperForms, self).tearDown()

    @params((Data.compraSimpleVisa, Data.validationVisa, True),)
    def test_Swatch_Approved(self, txData, validationData, expectedResult):

        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "C")
        self.runTx(txData, validationData)
        time.sleep(10)
        self.assertTxPPB(os.getenv("PPBLINK"), "approved", txData, validationData)

    @params((Data.compraSimpleVisa, Data.validationVisa_Rejected, False), )
    def test_Swatch_Rejected(self, txData, validationData, expectedResult):

        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "C")
        self.runTx(txData, validationData)
        time.sleep(10)
        self.assertTxPPB(os.getenv("PPBLINK"), "approved", txData, validationData)


    def runTx(self, txData, validationData):
        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           getFormsHash(txData, validationData)))
        template = TemplateSwatch(self.driver)
        self.fillTemplate(template, validationData)

        template.NROTARJETA.send_keys()

        time.sleep(15)
        template.SUBMIT.click()
        #template.SUBMIT.submit()

    def assertTxPPB(self, ppbLink, txStatus, txData, validationData):

        requestBin = RequestBin(self.driver)
        ppbData = json.loads (requestBin.getRawBody(txData["NROOPERACION"],ppbLink))

        assert_that(ppbData["payment"]["payment_method_id"], equal_to(int(txData["MEDIODEPAGO"])))
        assert_that(ppbData["payment"]["amount"], equal_to(int(txData["MONTO"])))
        assert_that(ppbData["payment"]["currency"], equal_to_ignoring_case("ARS"))
        assert_that(ppbData["payment"]["status"], equal_to_ignoring_case(txStatus))
        assert_that(ppbData["payment"]["customer"]["email"], equal_to_ignoring_case(validationData["EMAILCLIENTE"]))
        assert_that(ppbData["payment"]["installments"], equal_to(int(txData["CUOTAS"])))
        assert_that(ppbData["payment"]["site_id"], equal_to_ignoring_case(txData["NROCOMERCIO"]))