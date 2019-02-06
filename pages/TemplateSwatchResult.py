# -*- coding: utf-8 -*-
from pages.BasePage import BasePage
from datetime import datetime
import poormanslogging

class TemplateSwatchResult(BasePage):

    def __init__(self, driver):
        #BasePage.__init__(self,driver)
        self.driver = driver

    def getTxStatus(self):
        """Busca en pantalla el texto "¡Compra exitosa!". De esta forma, determina si el pago fue exitoso o no.
        """
        textResultSucess = self.driver.find_elements_by_xpath("//h3[@class='text-center result-success'][text()='¡Compra exitosa!']")
        return bool(textResultSucess)

    def getTxDetails(self):

        if self.getTxStatus():
            resultBody = self.driver.find_elements_by_css_selector(".jumbotron-body")[0]

            paymentInfo = {}
            paymentInfo["result"] = self.driver.find_element_by_css_selector(".text-center.result-success").text
            paymentInfo["resultDescription"] = self.driver.find_element_by_css_selector(".text-center").text
            paymentInfo["resultBodyFirstLine"] = resultBody.find_elements_by_tag_name("p")[0].text
            paymentInfo["resultBodySecondLine"] = resultBody.find_elements_by_tag_name("p")[1].text
            paymentInfo["authorizationCode"] = resultBody.find_elements_by_tag_name("p")[2].text
            paymentInfo["datetime"] = resultBody.find_elements_by_tag_name("p")[3].text

        elif not bool(self.driver.find_elements_by_css_selector(
                "//h3[@class='text-center result-error'][text()='Algo salió mal']")):
                raise Exception ("Pago errado")



        else:
            # Unknown result screen
            self.driver.get_screenshot_as_file("/screenshots/UnknownResultScreenOnSwatchPayment_{}.png".format(datetime.now()))
            poormanslogging.error("Unknown result screen after Swatch payment. Screenshoot was saved at")

        return paymentInfo

