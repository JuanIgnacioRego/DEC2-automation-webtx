from pages.BasePage import BasePage
from settings import *
import os
from tools import convertDictToWebTx,translationRequestBin_SAC
from hamcrest import *
from Exceptions import PPBNotFoundException
#TODO: openRequestBinLink(), deshardcodearlo.

class RequestBin(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)

    def generateMockLink(self):
        self.driver.get("http://{}:{}".format(environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["requestBin"]["baseURL"],
                                       environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["requestBin"]["port"]))
        createButton = self.driver.find_element_by_xpath("//a[@class='btn btn-success btn-large']")
        createButton.click()
        import time
        time.sleep(3)
        self.mockLink = self.driver.current_url.replace("?inspect", "").replace("localhost","marathon-lb.infrastructure.marathon.mesos")
        return self.mockLink


    def getTx(self, txId, ppbLink):
        ppbLink = ppbLink.replace("marathon-lb.infrastructure.marathon.mesos", "localhost")
        ppbLink = ppbLink.replace("request-bin", "localhost")
        ppbLink = ppbLink.replace("8000", "10113")
        self.driver.get (ppbLink+"?inspect")
        keyPairs = self.driver.find_elements_by_xpath("//*[text()=' {}']/../p[@class='keypair']".format(txId)) #don't delete that fucking space!
        values = {}
        for keyPair in keyPairs:
            keyPair = str(keyPair.text)
            values[keyPair[:keyPair.find(":")]] = keyPair[keyPair.find(":")+1:].strip()

        values = convertDictToWebTx(values, translationRequestBin_SAC)
        assert_that (txId, equal_to(values["NROOPERACION"]), "PPB was not made for tx id {}".format(txId))
        return values

    def __getTx(self, txId, ppbLink):
        ppbLink = ppbLink.replace("marathon-lb.infrastructure.marathon.mesos", "localhost")
        ppbLink = ppbLink.replace("request-bin", "localhost")
        ppbLink = ppbLink.replace("8000", "10113")
        self.driver.get(ppbLink + "?inspect")

        keyPairs = self.driver.find_elements_by_xpath(
            "//*[text()=' {}']/../p[@class='keypair']".format(txId))  # don't delete that fucking space!
        values = {}
        for keyPair in keyPairs:
            keyPair = str(keyPair.text)
            values[keyPair[:keyPair.find(":")]] = keyPair[keyPair.find(":") + 1:].strip()

        values = convertDictToWebTx(values, translationRequestBin_SAC)
        assert_that(txId, equal_to(values["NROOPERACION"]), "PPB was not made for tx id {}".format(txId))
        return values


    def getRawBody(self, data, ppbLink):
        self.openRequestBinLink(ppbLink)

        rawBodies = self.driver.find_elements_by_xpath("//pre[@class='body prettyprint']")
        for rawBody in rawBodies:
            if data in rawBody.text:
                return rawBody.text
        raise PPBNotFoundException("Data \"{}\" was not found as a raw body in RequestBin".format(data))

    def openRequestBinLink(self, ppbLink):
        """
        Redirects to tunneled RequestBin page, converting marathon-lb... to localhost
        :param ppbLink: link where post por background was made, using SAC valid structure (marathon-lb...:8000/link)
        """
        ppbLink = ppbLink.replace("marathon-lb.infrastructure.marathon.mesos", "localhost")
        ppbLink = ppbLink.replace("request-bin", "localhost")
        ppbLink = ppbLink.replace("8000", "10113")
        self.driver.get(ppbLink + "?inspect")