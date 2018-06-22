# -*- coding: utf-8 -*-
from pages.BasePage import BasePage

class Validation(BasePage):

    def __init__(self, driver, paymentMethod):
        self.driver = driver
        if paymentMethod == "1":
            self.__class__.__name__ = "ValidationVisa"
        if paymentMethod == "15":
            self.__class__.__name__ = "ValidationMastercard"
        if paymentMethod == "42":
            self.__class__.__name__ = "ValidationNativa"
        elif paymentMethod == "65":
            self.__class__.__name__ = "ValidationAmex"
        if self.wasApproved(): BasePage.__init__(self, self.driver)

    def wasApproved(self):
        """
        Return True if Tx was satisfactory
        Return False if there was an Error during Tx: 'Ha ocurrido un error en la operación:' will be shown in screen.
        """
        return len(self.driver.find_elements_by_xpath(".//font[text()='Ha ocurrido un error en la operación:']")) == 0

    def getSatisfactoryTxData(self, driver, paymentMethod, cardNumber):
        """
        Return a dict composed by satisfactory Tx validation data (Nombre, Email, Código de operación).
        "Código de autorización" and "Fecha/Hora" were ignored.
        """
        self.driver = driver
        satisfactoryTxData = self.driver.find_elements_by_xpath("//tbody/tr/td[2]")
        if paymentMethod == "1":
            return {
            "NOMBREENTARJETA": satisfactoryTxData[0].text,
            "EMAILCLIENTE":satisfactoryTxData[1].text,
            "NROOPERACION":satisfactoryTxData[3].text,
            "Tx_FechaYHora":satisfactoryTxData[2].text,
            "Tx_CodigoDeAutorizacion": satisfactoryTxData[4].text,
            }
        elif paymentMethod == "15":
            return{
            "NOMBREENTARJETA": satisfactoryTxData[2].text,
            "EMAILCLIENTE": satisfactoryTxData[3].text,
            "NROOPERACION": satisfactoryTxData[0].text,
            "Tx_FechaYHora": satisfactoryTxData[4].text,
            "Tx_CodigoDeAutorizacion": satisfactoryTxData[1].text
            }
        elif paymentMethod == "42" and cardNumber.startswith("4"): #NATIVA VISA
            return {
                "NOMBREENTARJETA": satisfactoryTxData[0].text,
                "EMAILCLIENTE": satisfactoryTxData[1].text,
                "NROOPERACION": satisfactoryTxData[3].text,
                "Tx_FechaYHora": satisfactoryTxData[2].text,
                "Tx_CodigoDeAutorizacion": satisfactoryTxData[4].text,
            }
        elif paymentMethod == "42" and cardNumber.startswith("5"): #NATIVA MASTERCARD
            return {
                "NOMBREENTARJETA": satisfactoryTxData[2].text,
                "EMAILCLIENTE": satisfactoryTxData[3].text,
                "NROOPERACION": satisfactoryTxData[0].text,
                "Tx_FechaYHora": satisfactoryTxData[4].text,
                "Tx_CodigoDeAutorizacion": satisfactoryTxData[1].text
            }
