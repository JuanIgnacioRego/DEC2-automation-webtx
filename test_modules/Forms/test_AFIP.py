# -*- coding: utf-8 -*-
from Exceptions import PPBNotFoundException
from test_modules.Forms.BaseTestForms import BaseTestForms
from pages.RequestBin import RequestBin
import Data
from nose2.tools.params import params
import os
from hamcrest import *
import QAPI
import json
import time
import random
import unittest
import DBConnection

#TODO: crear un siteId exclusivo para AFIP
#TODO: quedan pendientes algunas validaciones en PPB
#TODO: el generateVEP() da miedo... recursividad, please, avoid
#TODO: revisar en los assert, cuando revisa desde el param vep y cuando desde txData["nrooperacion"]
def generateVEP():
    vep = random.randint(1542401576,9999999999)
    tx = DBConnection.query("SELECT * \
                                FROM sps433.spstransac \
                                WHERE idtransaccionsite ='{}'"
                            .format(vep))
    if len(tx):
        vep = generateVEP()
    else:
        return str(vep)

class AFIP(BaseTestForms, unittest.TestCase):

    def setUp(self):
        super(AFIP, self).setUp()
        QAPI.setTimeoutPaymentForm(Data.forms_env["AFIP_SITE_ID"], 120)
        QAPI.unsetURLDinamica(Data.forms_env["AFIP_SITE_ID"], os.getenv("PPBLINK"), "A")

    def tearDown(self):
        super(AFIP, self).tearDown()
        QAPI.unsetURLDinamica(Data.forms_env["AFIP_SITE_ID"], os.getenv("PPBLINK"), "B")

    @params((Data.forms_env["ALIAS_KEY"], Data.txSimpleVisa_AFIP["NROOPERACION"], Data.txSimpleVisa_AFIP, Data.validationVisa_AFIP,
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
                                                       "auth_code"),
                                        "JSON fields")
        assert_that(jsonResponse["status"], equal_to_ignoring_case("0"),
                    "Tx statusId (0 = approved / 1 = rejected")
        assert_that(jsonResponse["response_message"], equal_to_ignoring_case(expectedTxStatus),
                    "Tx status description (Aprobada/Rechazada)")
        assert_that(jsonResponse["vendor_unique_id"], equal_to_ignoring_case(txData["NROOPERACION"]),
                    "Tx id (equal to VEP)")

        # Check tx in SAC
        self.assertTxInSAC(txData, validationData, expectedTxStatus)
        # Check tx PPB
        self.assertTxPPB(os.getenv("PPBLINK"), vep, txData, validationData)

    @params((Data.forms_env["ALIAS_KEY"], Data.txSimpleVisa_AFIP["NROOPERACION"], Data.txSimpleVisa_AFIP, Data.validationVisa_AFIP,
             "Rechazada"))
    def test_Payment_Rejected_RepeatedVEP(self, aliasKey, vep, txData, validationData, expectedTxStatus):
        self.runTx(aliasKey, vep, txData, validationData)
        jsonResponse = self.getJsonResult()
        # result = {"status": "1", "response_message": "Rechazada", "vendor_unique_id": "390229684"}
        assert_that(jsonResponse.keys(), only_contains("status",
                                                       "response_message",
                                                       "vendor_unique_id"),
                                            "JSON fields")
        assert_that(jsonResponse["status"], equal_to_ignoring_case("1"),
                    "Tx statusId (0 = approved / 1 = rejected")
        assert_that(jsonResponse["response_message"], equal_to_ignoring_case(expectedTxStatus),
                    "Tx status description (Aprobada/Rechazada)")
        assert_that(jsonResponse["vendor_unique_id"], equal_to_ignoring_case(txData["NROOPERACION"]),
                    "Tx id (equal to VEP)")

    @params((Data.forms_env["ALIAS_KEY"], generateVEP(), Data.txSimpleVisa_AFIP, Data.validationVisa_Rejected,
             "Rechazada"))
    def test_Payment_Rejected_RejectedCard(self, aliasKey, vep, txData, validationData, expectedTxStatus):

        self.runTx(aliasKey, vep, txData, validationData)
        jsonResponse = self.getJsonResult()
        # result = {"status": "1", "response_message": "Rechazada", "vendor_unique_id": "390229684"}
        assert_that(jsonResponse.keys(), only_contains("status",
                                                       "response_message",
                                                       "vendor_unique_id")
                                        , "JSON fields")
        assert_that(jsonResponse["status"], equal_to_ignoring_case("1"),
                    "Tx statusId (0 = approved / 1 = rejected")
        assert_that(jsonResponse["response_message"], equal_to_ignoring_case(expectedTxStatus),
                    "Tx status description (Aprobada/Rechazada)")
        assert_that(jsonResponse["vendor_unique_id"], equal_to_ignoring_case(vep),
                    "Tx id (equal to VEP)")

        assert_that(calling(self.assertTxPPB(os.getenv("PPBLINK"), vep, txData, validationData)),
                    raises(PPBNotFoundException),
                    "Check that PPB has not been made for rejected tx with id {}".format(vep))

    @params((Data.forms_env["ALIAS_KEY"], generateVEP(), Data.txSimpleVisa_AFIP, Data.validationVisa,
             "Rechazada"))
    def test_Payment_Rejected_TimeoutForm(self, aliasKey, vep, txData, validationData, expectedTxStatus):
        QAPI.setTimeoutPaymentForm(Data.forms_env["AFIP_SITE_ID"], 5)

        self.buildForm(aliasKey, vep, txData, validationData)
        self.fillForm(validationData)
        time.sleep(6)
        self.submitForm()

        expiredFormMessage = self.driver.find_element_by_xpath("//h1").text
        assert_that(expiredFormMessage, is_(equal_to("El formulario solicitado ha expirado")))

        QAPI.setTimeoutPaymentForm(Data.forms_env["AFIP_SITE_ID"], 120)

    def runTx(self, aliasKey, vep, txData, validationData):
        self.buildForm(aliasKey, vep, txData, validationData)
        self.fillForm(validationData)
        self.submitForm()

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

    def fillForm(self, validationData):
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

        """
        self.driver.find_element_by_id("NumeroTarjeta").send_keys(validationData["NROTARJETA"])
        self.driver.find_element_by_id("Nombre").send_keys(validationData["NOMBREENTARJETA"])
        #Son dos elementos con el mismo id
        self.driver.find_elements_by_id("FechaExpiracion")[0].send_keys(validationData["idComboMes"])
        self.driver.find_elements_by_id("FechaExpiracion")[1].send_keys(validationData["idComboAno"])
        self.driver.find_elements_by_id("cvc")[0].send_keys(validationData["CODSEGURIDAD"])
        self.driver.find_elements_by_id("boton-pagar")[0].submit()
        """

    def submitForm(self):
        self.driver.execute_script(
            "document.getElementById('boton-pagar').click()")

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


