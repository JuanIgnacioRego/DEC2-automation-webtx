# -*- coding: utf-8 -*-
from pages.BasePage import BasePage
from tools import TraduccionCamposWebTx_SAC
"""
class SACTxHistory(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self,driver)

    def consultarTransaccion(self, id):
        return (self.driver.find_elements_by_xpath("//*[text()='"+id+"']/../td") > 0)

    def obtenerCamposDeTransaccion(self):
        """
        #Devuelve una lista con los nombres de los campos de una Tx de SAC:
        #["Conf", "ID Op.", "Fecha última modif.", "Fecha original", "Monto",...]
        """
        return (list(map(lambda td: td.text, self.driver.find_elements_by_xpath("//tr[@class='txtazulchicobold']/td"))))

    def getTxFieldNames(self):
        """
        #:return: a list containing tuples describing a fieldName and its position on SAC's fields list.
        """
        fieldNames = self.driver.find_elements_by_xpath("//tr[@class='txtazulchicobold']/td")
        fieldTuples = []
        for i in range (fieldNames):
            fieldTuples.append( (fieldNames[i], i) )
        return fieldTuples

    def getTx(self, txId):
        """
        #:param txId: id of transaction
        #:return: a dict with structure txFieldName : txFieldValue
        """
        tx = {}
        consideredFields = [field for field in self.getTxFieldNames() if field[0] in TraduccionCamposWebTx_SAC.keys()]
        for field in consideredFields:
            tx [field] = self.driver.find_elements_by_xpath("//*[text()='"+id+"']/../td["+field[1]+"]").text

        return tx




    def obtenerTransaccion(self, id):
        """
        #Devuelve un diccionario en el que se componen los distintos campos de una transacción.
        """
        transaccion = {}
        for i in range(len(self.obtenerCamposDeTransaccion())):
            transaccion[self.getTxFieldsNames()[i]] = self.driver.find_elements_by_xpath("//*[text()='"+id+"']/../td")[i].text
        
        
        return transaccion

    def getTxMATCH(self, id):
        rawTx = self.obtenerTransaccion(id)
        tx = dict()
        #It start taking those fields that I consider important to be verified

        importantFields = list(set(rawTx.keys()).intersection(TraduccionCamposWebTx_SAC.keys()))

        for field in importantFields:
            tx [TraduccionCamposWebTx_SAC[field]] = rawTx[field]

        return tx
"""