import os
import requests
from settings import *
import time
import DBConnection
import json
from Exceptions import URLStatusCodeNot200Exception

baseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["QAPI"]["baseURL"]
port = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["QAPI"]["port"]
coreTxBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["coreTx"]["baseURL"]
coreTxPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["coreTx"]["port"]
formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]

def getIturanHash(txData, validationData):

    headers = {"X-Consumer-Username":"{}_pci".format(txData["NROCOMERCIO"])}

    response = requests.post(("http://{}:{}/validate").format(formsBaseURL, formsPort),headers = headers,
               json={
                   "site": {
                       #"id": txData["NROCOMERCIO"],
                       "transaction_id": txData["NROOPERACION"]
                   }
                   ,
                   "customer": {
                       "id": "Morton",
                       "email": validationData["EMAILCLIENTE"]
                   },
                   "payment": {
                       "amount": int(txData["MONTO"]),
                       "currency": "ARS",
                       "payment_method_id": int(txData["MEDIODEPAGO"]),
                       "installments": int(txData["CUOTAS"]),
                       "payment_type": "single",
                       "sub_payments": []
                   },
                   "success_url": "http://www.ituran.com.ar/home",
                   "cancel_url": "http://www.ituran.com.ar/pagos"
               })

    if response.ok:
        return (response.json()["hash"])
    else:
        print (response.text)

def getSwatchHash(txData, validationData):

    headers = {
        "Content-Type":"application/json",
        "X-Consumer-Username":"{}_pci".format(txData["siteId"])
    }


    response = requests.post(("http://{}:{}/validate").format(formsBaseURL, formsPort),
                             headers = headers,
                             json = validationData)
    """
    response = requests.post(("http://{}:{}/validate").format(formsBaseURL, formsPort),headers = headers,
               json={
                 "site": {
                     #"id": txData["NROCOMERCIO"],
                     "transaction_id": "Swatch {}".format(txData["NROOPERACION"]),
                     "template": {
                         "id": 4
                     }
                 },
                 "customer": {
                     "id": "001",
                     "email" : validationData["EMAILCLIENTE"]
                 },
                 "payment": {
                     "amount": int(txData["MONTO"]),
                     "currency": "ARS",
                     "payment_method_id":int(txData["MEDIODEPAGO"]),
                     #"bin": validationData["NROTARJETA"][:6],
                     "installments" : int(txData["CUOTAS"]),
                     "payment_type": "single",
                     "sub_payments" : []
                 },
                 "success_url": "http://www.redbee.io/",
                 "cancel_url": "https://shop.swatch.com/es_ar/"
                }
    )
    """

    return response
    """
    if response.ok:
        return (response.json()["hash"])
    else:
        raise URLStatusCodeNot200Exception(response.status_code, response.text)
    """