# -*- coding: utf-8 -*-

from Exceptions import PPBNotFoundException, URLStatusCodeNot200Exception
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
from services.Forms import getSwatchHash
from pages.TemplateSwatch import TemplateSwatch
from pages.TemplateSwatchResult import TemplateSwatchResult

class Swatch(BaseTestForms, unittest.TestCase):

    #SBR: it was for Layers implementation, but it was avoided finally:
    #layer = LayerSwatch

    @params((Data.txSimpleVisa_Swatch, Data.validationData_Swatch, True),)
    def test_Swatch_Approved(self, txData, validationData, expectedResult):
        QAPI.unsetURLDinamica(Data.sites["Swatch"], os.getenv("PPBLINK"), "C")

        self.runTx(txData, validationData)
        #self.assertResultScreen()
        self.assertTxPPB(os.getenv("PPBLINK"), "approved", txData, validationData, txId=validationData["site"]["transaction_id"])

    @params((Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_DigitalGoods, True, "DigitalGoods"),
            (Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_Retail, True, "Retail"),
            (Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_Services, True, "Services"),
            (Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_Ticketing, True, "Ticketing"),
            (Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_Travel, True, "Travel"),
            (Data.txSimpleVisa_Swatch, Data.validationData_Swatch_CS_RetailTP, True, "RetailTP")
             )
    def test_Swatch_CS_Approved(self, txData, validationData, expectedResult, vertical):

        # se podra borrar el expected result?
        # buscar alguna forma de setear 1 vez el UNSET URL dinamica y listo, se repite en todos los test
        QAPI.unsetURLDinamica(Data.sites["Swatch"], os.getenv("PPBLINK"), "C")
        QAPI.setCS(siteId=txData["NROCOMERCIO"], vertical= vertical)
        time.sleep(3)

        self.runTx(txData, validationData)
        # self.assertResultScreen()
        # self.assertTxInSAC()
        self.assertTxPPB(os.getenv("PPBLINK"), "approved", txData, validationData,
                         txId=validationData["site"]["transaction_id"])

        QAPI.unsetCS(siteId=txData["NROCOMERCIO"])

    def test_Swatch_CancelURL_ParamNotSent(self, txData=Data.txSimpleVisa_Swatch, validationData=Data.validationData_Swatch):
        self.validationData = validationData.copy()
        self.validationData.pop("cancel_url")

        response = getSwatchHash(txData, self.validationData)

        try:
            assert_that(response.status_code, is_(equal_to(400)),
                        "Hash shouldn't be generated when cancel_url parm is not sent. It was generated anyway.")
            assert_that(response.json()["validation_errors"][0]["code"], is_(equal_to("param_required")))
            assert_that(response.json()["validation_errors"][0]["param"], is_ (equal_to("cancel_url")))
        except AssertionError:
            print("Assertion failed.\nResponse status: {}\nResponse message: {}"
                .format(response.status_code, response.text))
            raise

    def test_Swatch_CancelURL_EmptyParam(self, txData=Data.txSimpleVisa_Swatch, validationData=Data.validationData_Swatch):
        self.validationData = validationData.copy()
        self.validationData["cancel_url"] = ""

        response = getSwatchHash(txData, self.validationData)

        try:
            assert_that(response.status_code, is_(equal_to(400)),
                    "Hash shouldn't be generated when cancel_url is sent as empty. It was generated anyway.")
            assert_that(response.json()["validation_errors"][0]["code"], is_(equal_to("invalid_param")))
            assert_that(response.json()["validation_errors"][0]["param"], is_ (equal_to("cancel_url")))
        except AssertionError:
            print("Assertion failed.\nResponse status: {}\nResponse message: {}"
                .format(response.status_code, response.text))
            raise

    @params((" ",),
            ("http://",),
            ("www.",),
            ("http://a",),
            ("http://@.com",),
            ("http://esto es una url espaciada.com",))
    def test_Swatch_CancelURL_InvalidParam(self, cancelURL, txData=Data.txSimpleVisa_Swatch, validationData=Data.validationData_Swatch):
        self.validationData = validationData.copy()
        self.validationData["cancel_url"] = cancelURL

        response = getSwatchHash(txData, self.validationData)

        try:
            assert_that(response.status_code, is_(equal_to(400)),
                        "Hash shouldn't be generated when cancel_url is invalid. It was generated anyway using {} as cancel_url.".format(cancelURL))
            assert_that(response.json()["validation_errors"][0]["code"], is_(equal_to("invalid_param")))
            assert_that(response.json()["validation_errors"][0]["param"], is_(equal_to("cancel_url")))
        except AssertionError:
            print("Assertion failed.\nResponse status: {}\nResponse message: {}"
                .format(response.status_code, response.text))
            raise

    def notest_Swatch_CancelURL_PaymentCanceled(self, txData=Data.txSimpleVisa_Swatch, validationData=Data.validationData_Swatch):
        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL,
                                                           self.formsPort,
                                                           getSwatchHash(txData, validationData)))

        template = TemplateSwatch(self.driver)
        self.fillTemplate(template, txData)
        template.cancel.click()
        assert_that(self.driver.current_url, is_(equal_to(validationData["cancel_url"])))

    def notest_Swatch_RedirectURL(self, txData=Data.txSimpleVisa_Swatch, validationData=Data.validationData_Swatch_RedirectURL):
        from tools import Schemas
        QAPI.setCardNumberFormat("####XXXXXXXX####")

        self.runTx(txData, validationData)
        assert_that(self.driver.current_url.startswith(validationData["redirect_url"]))

        decodedJSON = self.getDecodedJSONFromRedirectURL(self.driver.current_url)
        self.assertJSONSchema (decodedJSON, Schemas.redirectURLEncodedJSON)
        self.assertCardNumberMask()
        self.assertTxInSAC()
        self.assertTxPPB()

    @params((Data.compraSimpleVisa, Data.validationVisa, True), )
    def notest_Swatch_PaymentFormValidations(self, txData, validationData, expectedResult):
        def getCardNumberError():
            return self.driver.find_elements_by_id("cardNumberError")


        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL,
                                                           self.formsPort,
                                                           getSwatchHash(txData, validationData)))

        template = TemplateSwatch(self.driver)

        #1
        template.cardNumber.send_keys("Esto seria invalido")
        assert_that(template.cardNumber.text, is_(""))
        assert_that

        #2
        template.cardNumber.send_keys("41234567891234567890")
        assert_that(template.cardNumber.text, is_("4123 4567 8912 3456"))
        template.cardNumber.clear()
        template.cardNumber.send_keys("4123456789123")
        assert_that(template.cardNumber.text, is_("41234 5678 9123"))

        template.cardExpiration.send_keys("ENERO")
        assert_that(template.cardExpiration.text, is_(""))

        template.cardExpiration.send_keys()


        raise Exception()

    @params((Data.compraSimpleVisa, Data.validationVisa_Rejected, False), )
    def notest_Swatch_Rejected(self, txData, validationData, expectedResult):

        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "C")
        self.runTx(txData, validationData)
        time.sleep(10)
        self.assertTxPPB(os.getenv("PPBLINK"), "approved", txData, validationData)


    def runTx(self, txData, validationData):
        swatchValidateResponse = getSwatchHash(txData, validationData)
        try:
            assert_that(swatchValidateResponse.ok)
        except AssertionError as ae:
            print ("{}\nStatus code: {}.\nMessage:{}".format
            (ae, swatchValidateResponse.status_code, swatchValidateResponse.text))

        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL,
                                                           self.formsPort,
                                                           swatchValidateResponse.json()["hash"]))


        template = TemplateSwatch(self.driver)
        self.fillTemplate(template, txData)
        #SBR:
        template.cardHolderName.click()
        template.submit.click()

    def assertResultScreen(self):
        pass

    def assertTxPPB(self, ppbLink, txStatus, txData, validationData, txId=""):

        requestBin = RequestBin(self.driver)
        ppbData = json.loads (requestBin.getRawBody(txId if txId else txData["NROOPERACION"], ppbLink))

        assert_that(ppbData["payment"]["payment_method_id"], equal_to(int(validationData["payment"]["payment_method_id"])))
        assert_that(ppbData["payment"]["amount"], equal_to(int(validationData["payment"]["amount"])))
        assert_that(ppbData["payment"]["currency"], equal_to_ignoring_case("ARS"))
        assert_that(ppbData["payment"]["status"], equal_to_ignoring_case(txStatus))
        assert_that(ppbData["payment"]["customer"]["email"], equal_to_ignoring_case(validationData["customer"]["email"]))
        assert_that(ppbData["payment"]["installments"], equal_to(int(validationData["payment"]["installments"])))
        assert_that(ppbData["payment"]["site_id"], equal_to_ignoring_case(txData["siteId"]))

    def getDecodedJSONFromRedirectURL(self, redirectURL):
        import base64
        assert_that("result=" in redirectURL, "redirectURL was not generated correctly")

        redirectURL = str(redirectURL.decode("utf-8"))
        encodedJSON = redirectURL[str.rindex(redirectURL, "result=") + len("result="):]

        decodedJSON = base64.b64decode(encodedJSON + "==") #Si se elimina el +"==", devuelve padding_error.
        decodedJSON = decodedJSON.decode("utf-8")
        decodedJSON = json.loads(decodedJSON)

        return (decodedJSON)

    def assertJSONSchema(self, json, schema):
        from jsonschema import validate
        validate(json, schema)


