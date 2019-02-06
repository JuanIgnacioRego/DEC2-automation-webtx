# -*- coding: utf-8 -*-
#TODO: revisar services.Forms.getIturanHash
#TODO: reformularizar assertTxPPB para que cuando no encuentra el txID buscado devuelva una Execption
#TODO: en base a lo anterior verificar que la tx rechazada NO haga PPB
#TODO: hacer que el assertTxPPB tenga retries cada 15s, a veces se hace el PPB pero se chequea demasiado pronto.
from pages.TemplateIturan import TemplateIturan
from pages.TemplateIturanResult import TemplateIturanResult
import Data
from nose2.tools.params import params
import os
import unittest
from hamcrest import *
import QAPI
from Exceptions import *
import poormanslogging as log
import time
from test_modules.Forms.BaseTestForms import BaseTestForms
import services.Forms




class Ituran(BaseTestForms, unittest.TestCase):

    def runTx(self, txData, validationData):
        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           services.Forms.getIturanHash(txData, validationData)))
        template = TemplateIturan(self.driver)
        self.fillTemplate(template, validationData)
        template.SUBMIT.click()

    def temporizedRunTx(self, txData, validationData, customTimeout, timeToWait):
        import datetime
        import operator

        if customTimeout:
            QAPI.setTimeoutPaymentForm(txData["NROCOMERCIO"], customTimeout)

        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           services.Forms.getIturanHash(txData, validationData)))

        log.debug("WebDriver opened the form")
        template = TemplateIturan(self.driver)
        self.fillTemplate(template, validationData)
        log.debug("WebDriver have just filled the form")

        if timeToWait:
            timeToGenerateTimeOutError = datetime.datetime.now() + datetime.timedelta(0, timeToWait)
            log.debug("Starting counting time")
            log.wait_until("Waiting for timeout, {} secs".format(timeToWait),
                       lambda: datetime.datetime.now() < timeToGenerateTimeOutError,
                       operator.eq, False, 1)
            log.debug("Finishing counting time")

        template.SUBMIT.click()
        """Se establece el tiempo de vida del formulario por defecto (spssites.timeoutcompra =0, toma el valor de la variable de entorno FORM_TIMEOUT_SECONDS). Se procede a realizar un pago exitoso, pasados 45 segundos."""
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.temporizedRunTx(txData, validationData, customTimeout, customTimeout)

        expiredFormMessage = self.driver.find_element_by_xpath("//h1").text

    @params((Data.compraSimpleVisa, Data.validationVisa, True),)
    def test_Approved(self, txData, validationData, expectedResult, expectedTxStatus="Autorizada"):
        """Una tx exitosa vía Ituran. Se verifica que una vez aprobado el pago, se visualice en el SAC y realice el PPB. """
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        QAPI.unsetURLDinamica(txData["NROCOMERCIO"], os.getenv("PPBLINK"), "B")
        self.runTx(txData, validationData)

        templateTxResult = TemplateIturanResult(self.driver)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")
        txId, txAmount, txDate = templateTxResult.getTxResultDetails()
        assert_that(str(int(txAmount.replace("$", "").replace(".", ""))), txData["MONTO"], "Tx amount")
        assert_that(txDate, time.strftime('%d/%m/%Y'), "Tx date")
        self.assertTxInSAC(txData, validationData)
        time.sleep(7)
        self.assertTxPPB(txData, expectedTxStatus)

    @params((Data.compraSimpleVisa, Data.validationVisa_ExpiredCard, False),)
    def test_Rejected_ExpiredCard(self, txData, validationData, expectedResult):
        """Una tx no exitosa, usando una tarjeta con fecha de vencimiento expirada. Se verifica que no figure en el SAC."""
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData, validationData)

        templateTxResult = TemplateIturanResult(self.driver)
        time.sleep(3)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")
        assert_that(calling(self.assertTxInSAC).with_args(txData, validationData), raises(TxNotFoundInSACError))

    @params(
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_54, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_05, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_03, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_04, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_01, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_07, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_76, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_43, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_91, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_96, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_12, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_48, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_54, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_56, False),
        (Data.compraSimpleVisa, Data.validationVisa_Rejected_13, False),
    )
    def avoidtest_Rejected_BrandMessages(self, txData, validationData, expectedResult):
        """Se realizan tx con tarjetas que rechazan pagos. El objetivo es que se devuelva "RECHAZADA" como mensaje,\
         y no el motivo que devuelve la marca."""
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        self.runTx(txData, validationData)

        templateTxResult = TemplateIturanResult(self.driver)
        time.sleep(3)
        assert_that(templateTxResult.getTxStatus(), is_(expectedResult), "Tx status (approved/rejected)")
        assert_that(templateTxResult.getTxResultDetails(),
                    is_("RECHAZADA"))

    @params((Data.compraSimpleVisa, Data.validationVisa, True, 15.0), )
    def test_Approved_TimeoutPaymentForm_CustomValue(self, txData, validationData, expectedResult, customTimeout):
        """Se establece el tiempo de vida del formulario en 15 segundos, específicamente para el site \
        en el que se realiza la prueba. Se procede a realizar un pago exitoso, \
        dentro de esos 15 segundos."""
        QAPI.setTimeoutPaymentForm(txData["NROCOMERCIO"], customTimeout)
        self.test_Approved(txData, validationData, expectedResult)
        #Se retorna al timeout por defecto para el site en cuestión.
        QAPI.setTimeoutPaymentForm(txData["NROCOMERCIO"], 120.0)

    @params((Data.compraSimpleVisa, Data.validationVisa, False, 15.0),)
    def test_Failed_TimeoutPaymentForm_CustomValue_ExpiredForm(self, txData, validationData, expectedResult, customTimeout):
        """Con el tiempo de vida del formulario en 15 segundos, se intenta realizar una tx pasado este tiempo. La tx debe ser fallida."""
        txData["NROOPERACION"] = "ITURAN " + str(int(time.time()))
        QAPI.setTimeoutPaymentForm(txData["NROCOMERCIO"], customTimeout)

        import datetime
        import operator
        self.driver.get("http://{}:{}/form?hash={}".format(self.formsBaseURL, self.formsPort,
                                                           services.Forms.getIturanHash(txData, validationData)))

        #log.debug("WebDriver opened the form")
        template = TemplateIturan(self.driver)
        self.fillTemplate(template, validationData)
        #log.debug("WebDriver have just filled the form")

        timeToGenerateTimeOutError = datetime.datetime.now() + datetime.timedelta(0, customTimeout)
        #log.debug("Starting counting time")
        log.wait_until("Waiting for timeout, {} secs".format(customTimeout),
                       lambda: datetime.datetime.now() < timeToGenerateTimeOutError,
                       operator.eq, False, 1)
        #log.debug("Finishing counting time")
        template.SUBMIT.click()

        expiredFormMessage = self.driver.find_element_by_xpath("//h1").text
        assert_that(expiredFormMessage, is_(equal_to("El formulario solicitado ha expirado")))
        QAPI.setTimeoutPaymentForm(txData["NROCOMERCIO"], 120.0)