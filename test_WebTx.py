# -*- coding: utf-8 -*-

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pages.TemplateCompraSimple import TemplateCompraSimple
from pages.TemplateCompraDistribuida import TemplateCompraDistribuida
from pages.TemplateTxConAgregador import TemplateTxConAgregador
from pages.Validation import Validation
from pages.SACLogin import SACLogin
from pages.SACInicio import SACInicio
from pages.SAC import SACTxHistory
from pages.ConfirmTx import  ConfirmTx
from pages.RequestBin import RequestBin
import Data
from tools import TraduccionCamposWebTx_SAC, processData
from nose2.tools.params import params
import os
from settings import *
import unittest
from hamcrest import *
import QAPI
import time

# TODO: corregir los casos en los que se reescribe el txData["NROOPERACION"] para evitar el problema de idRepetido
# TODO: antes de correr los test, en el setUp(), agregar QAPI.removeMPOS y .removeCS
# TODO: generar una variable params, que tenga las tuplas
# TODO: manejo de errores: captura de pantalla y dejar abierto webdriver


class BaseTest(object):

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
        self.driver.quit()
        #pass

    def runTx(self, txData, validationData, txTemplate):
        template = txTemplate(self.driver, self.baseURL, self.port)
        self.fillTemplate(template, txData)
        template.SUBMIT.click()

        validation = Validation(self.driver, txData["MEDIODEPAGO"])
        satisfactoryTxData = {}
        if validation.wasApproved():
            self.fillTemplate(validation, validationData)
            time.sleep(3)
            validation.SUBMIT.click()
            if validationData["NROTARJETA"].startswith("5"):
                confirmTx = ConfirmTx(self.driver)
                confirmTx.CONFIRMAR.click()

            #It verifies the tx data that is displayed on screen when it was satisfactory.
            satisfactoryTxData = validation.getSatisfactoryTxData(self.driver, txData["MEDIODEPAGO"],
                                                                  validationData["NROTARJETA"])
            for key in list(set(txData.keys() + validationData.keys()).intersection(satisfactoryTxData.keys())):
                assert_that(txData[key] if txData.has_key(key) else validationData[key],
                            equal_to(satisfactoryTxData[key]), "Tx data, {} assertion".format(key))

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

