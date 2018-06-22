# -*- coding: utf-8 -*-
from pages.BasePage import BasePage
from tools import TraduccionCamposWebTx_SAC
import DBConnection as DB
from Exceptions import *

class SACTxHistory(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self, driver)
        self.consideredFields = [field for field in self.getTxFieldNames() if field[0] in TraduccionCamposWebTx_SAC.keys()]

    def getTxFieldNames(self):
        """
        :return: a list containing tuples describing a fieldName and its order number on SAC's fields list. For example:
                [(u'Conf.', 0), (u'ID op.', 1), (u'Fecha \xfaltima modif.', 2), (u'Fecha original', 3), ...]
        """
        fieldNames = self.driver.find_elements_by_xpath("//tr[@class='txtazulchicobold']/td")
        fieldTuples = []
        for i in range (len(fieldNames)):
            fieldTuples.append( (fieldNames[i].text, i) )

        return fieldTuples

    def getTx(self, txId, isFatherTx=False, consideredFields=''):
        """
        :param: txId: id of transaction
        :param: isFatherTx: if tx has subtransactions or not (like a distributed one)
        :return: transactions found with same txId.
                If only one tx is found, this method will return a dict that refers to that tx (used for simple txs).
                If several txs are found, this method will return a list containing dicts that refers to those txs
                (used for simple txs that compose a distributed one).
                If no txs are found, TxNotFoundInSAC will be raised.
        """
        txs = []

        if isFatherTx:
            sacTxRows = self.driver.find_elements_by_xpath(("//a[text()='{}']/../..").format(txId))
        else:
            sacTxRows = self.driver.find_elements_by_xpath(("//td[text()='{}']/..").format(txId))

        if not len(sacTxRows): raise TxNotFoundInSACError("The txId {} was not found in SAC. "
                                                          "Please refresh Redis keys."
                                                          .format(txId))

        for sacTxRow in sacTxRows:
            tx = {}
            for field in self.consideredFields:
                #Consider that xpath estructur element[0] would retrieve an error. Positional index elements start with [1]
                #tx [TraduccionCamposWebTx_SAC[field[0]]] = sacTxRow.find_element_by_xpath((".//*[text()='{}']/../td[{}]").format(txId, field[1]+1)).text
                tx[TraduccionCamposWebTx_SAC[field[0]]] = sacTxRow.find_element_by_xpath(
                    (".//td[{}]").format(field[1] + 1)).text
            txs.append(tx)

        txs = list (map(self.uglify, txs))
        return txs if len(txs)>1 else txs[0]

    def getDistributedTx(self, txId):
        """
        :param txId: id of transaction
        :return: a list whose first element is the distributed tx, and remaining ones are its simple txs
        """
        txs = []
        distributedTx = {}
        for field in self.consideredFields:
            # Consider that xpath structure element[0] would retrieve an error. Positional index elements start with [1]
            distributedTx[TraduccionCamposWebTx_SAC[field[0]]] = self.driver.find_element_by_xpath(("//a[text()='{}']/../../td[{}]").format(txId, field[1]+1)).text
        txs.append(self.uglify(distributedTx))

        #The following line clicks on distributed tx link to expand its simple txs
        self.driver.find_element_by_xpath(("//a[text()='{}']").format(txId)).click()

        #Get simple txs that compose the distributed one
        txs = txs + self.getTx(txId)
        return txs

    def uglify(self, tx):
        """
        :param tx: a tx (whose structure is a dict)
        :return: same tx but in WebTx format. For example, an amount of "$ 1.00" is going to be converted to "100"
        """
        tx ["MONTO"] = str(int(tx["MONTO"].replace("$","").replace(".","")))
        tx ["NROCOMERCIO"] = DB.query ("SELECT idsite FROM spssites WHERE descri = '{}'".format(tx ["NROCOMERCIO"]))[0]['idsite']
        return tx

    def getTxFullData(self, txId, isFatherTx=False):
        # TODO: este metodo esta bastante fiero, es una copia de codigo de getTx(). Hay que mejorarlo
        """
        :return: a dict{} with structure fieldName:value for all SAC fields.
                getTx() returns a tx with same structure but only some specefic fields
                (defined on TraduccionCamposWebTx_SAC).
                In contrast to getTx(), getTxFullData() returns all SAC fields.

        :param: txId: id of transaction
        """
        fieldsToIgnore = ["Conf.", "Resultado CS", "Operaciones"]
        fields = [field for field in self.getTxFieldNames() if field not in fieldsToIgnore]

        if isFatherTx:
            sacTxRow = self.driver.find_element_by_xpath(("//a[text()='{}']/../..").format(txId))
        else:
            sacTxRow = self.driver.find_element_by_xpath(("//td[text()='{}']/..").format(txId))
        tx = {}
        for field in fields:
            # Consider that xpath estructur element[0] would retrieve an error. Positional index elements start with [1]
            # tx [TraduccionCamposWebTx_SAC[field[0]]] = sacTxRow.find_element_by_xpath((".//*[text()='{}']/../td[{}]").format(txId, field[1]+1)).text
            tx[field[0]] = sacTxRow.find_element_by_xpath(
                (".//td[{}]").format(field[1] + 1)).text

        return tx

    def getTxStatus(self, txId, isFatherTx=False):
        """
        :param txId:id of transaction
        :return: tx status: "Autorizada", "Pre autorizada", "Rechazada"
        """
        return self.getTxFullData(txId, isFatherTx)["Estado"]
