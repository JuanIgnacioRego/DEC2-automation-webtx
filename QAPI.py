import os
import requests
from settings import *
import time
import DBConnection
import json

baseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["QAPI"]["baseURL"]
port = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["QAPI"]["port"]
coreTxBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["coreTx"]["baseURL"]
coreTxPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["coreTx"]["port"]
formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]
marathonAPIBaseURL = "localhost"
marathonAPIPort = "18082"

def setDistributedTxByPercentage(siteId):
    response = requests.post(("http://{}:{}/sites/porcentaje").format(baseURL, port),
                  json={
                        "site": siteId
                        })

    if response.ok: replicate(siteId)

def unsetDistributedTxByPercentage(siteId):
    response = requests.delete(("http://{}:{}/sites/porcentaje").format(baseURL, port),
                             json={
                                 "site": siteId
                             })

    if response.ok: replicate(siteId)

def addSubsites(siteId, subsitesIds):
    response = requests.post(("http://{}:{}/sites/subsites").format(baseURL, port),
                json ={
                    "site": siteId,
                    "subsites": subsitesIds
                })

    if response.ok: replicate(siteId)

def deleteSubsites(siteId, subsitesIds=""):
    response = requests.delete(("http://{}:{}/sites/subsites").format(baseURL, port),
                             json={
                                 "site": siteId,
                                 "subsites": subsitesIds
                             })
    if response.ok: replicate(siteId)

def unsetCS(siteId):
    response = requests.delete(("http://{}:{}/sites/cs").format(baseURL, port),
                               json={
                                   "site": siteId
                               })
    if response.ok: replicate(siteId)

def replicate(siteId):
    replicationResponse = requests.get(("http://{}:{}/replication/site/{}").format(coreTxBaseURL, coreTxPort, siteId))

def setTxInTwoSteps(siteId, paymentMethodId):
    response = requests.post(("http://{}:{}/sites/dospasos").format(baseURL, port),
                json={
                    "site": siteId,
                    "medio_de_pago": paymentMethodId
                    })
    if response.ok: replicate(siteId)

def unsetTxInTwoSteps(siteId, paymentMethodId):
    response = requests.delete(("http://{}:{}/sites/dospasos").format(baseURL, port),
                json={
                    "site": siteId,
                    "medio_de_pago": paymentMethodId
                    })
    if response.ok: replicate(siteId)

def setURLDinamica(siteId, mode):
    response = requests.post(("http://{}:{}/sites/urldinamica").format(baseURL, port),
                             json={
                                 "site": siteId,
                                 "mode":mode
                             })
    if response.ok: replicate(siteId)

def unsetURLDinamica(siteId, url, mode):
    response = requests.delete(("http://{}:{}/sites/urldinamica").format(baseURL, port),
                             json={
                                 "site": siteId,
                                 "url": url,
                                 "mode": mode
                             })
    if response.ok: replicate(siteId)

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

def getVepJSONObject(vep):
    response = requests.get(("http://{}:{}/vep/{}").format(baseURL, port,vep))
    if response.ok:
        return json.loads(response.text)

def getVersionApps():
    response = requests.get("http://{}:{}/v2/apps".format(marathonAPIBaseURL, marathonAPIPort))
    versionApps = []
    if response.ok:
        for app in response.json()["apps"]:
            if app["id"].startswith("/decidir/") and isinstance(app["container"], dict):
                print ("{}: {}".format(app["id"], app["container"]["docker"]["image"]))
    else:
        print (response.text)

def getPercentagesConfiguration(siteId):
    """
    Get father site and its subsites percentages configuration in a list structure composed by tuples
    [("siteId", "percentage"), [("subsite1", "percentage")], ...]
    """
    subsitesPercentages = DBConnection.query("SELECT idsubsite, porcentaje \
                                            FROM spssites_subsites \
                                            WHERE idsite ={} \
                                            AND activo = 'S'"
                                             .format(siteId))

    sumPercentages = sum([subsite["porcentaje"] for subsite in subsitesPercentages])
    percentagesConfiguration = {}
    percentagesConfiguration[siteId] = round(100-sumPercentages,2) #Father site
    for subsite in subsitesPercentages:
        percentagesConfiguration[subsite["idsubsite"]] = subsite["porcentaje"]

    return percentagesConfiguration

def getTxFromDB(txId):
    tx = DBConnection.query("SELECT * \
                            FROM sps433.spstransac \
                            WHERE idtransaccionsite ='{}'"
                         .format(txId))
    if len(tx)<1:
        raise Exception ("Tx was not found in DB with txId = {}".format(txId))
    elif len(tx) >1:
        raise Warning("Tx was found more than once in DB with txId = {}".format(txId))

    return tx[0]

def getCurrency(currencyId):
    currency = DBConnection.query("SELECT * \
                            FROM sps433.spsmonedas \
                            WHERE idmoneda ={}"
                         .format(currencyId))
    if len(currency)<1:
        raise Exception ("Currency was not found in DB with id = {}".format(currencyId))
    return currency[0]