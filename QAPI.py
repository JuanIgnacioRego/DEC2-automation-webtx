import os
import requests
from settings import *
import time
import DBConnection
import json
from Data import CyberSource as CS
from Exceptions import URLStatusCodeNot200Exception

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

def setCS(siteId, vertical, securityKey="", mid="decidir_agregador", modelo="2", continuarFaltandoDatosRequeridos="N", reversoAutomaticoIndisponibilidadCS="N"):
    response = requests.post("http://{}:{}/sites/cs".format(baseURL, port),
                             json={
                                 "site": siteId,
                                 "security_key": securityKey if securityKey else CS["securityKey"],
                                 "modelo": modelo,
                                 "mid": mid,
                                 "rubro": CS["verticales"][vertical],
                                 "continuar": continuarFaltandoDatosRequeridos,
                                 "reverso": reversoAutomaticoIndisponibilidadCS
                             })
    if response.ok:
        replicate(siteId)
    else:
        raise URLStatusCodeNot200Exception("HTTP status not OK after requesting. Status received is {}: \n {}".format(
            response.status_code, response.text))



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
    if response.ok:
        replicate(siteId)
    else:
        raise URLStatusCodeNot200Exception ("Status received:{}".format(response.text))

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

def setTimeoutPaymentForm(siteId, timeoutInMiliseconds):
    timeout = DBConnection.query("UPDATE sps433.spssites \
                                  SET timeoutcompra = {} \
                                    WHERE idsite = {}"
                                  .format(timeoutInMiliseconds, siteId))

    replicate(siteId)

def getTimeoutPaymentForm(siteId):
        timeout = DBConnection.query("SELECT timeoutcompra \
                                     FROM sps433.spssites \
                                    WHERE idsite = {}"
                                     .format(siteId))

        return (timeout)

def setCardNumberFormat(siteId, paymentMethodId, cardNumberFormat):
    DBConnection.query("UPDATE sps433.spsmedpagotienda \
                                SET FORMATONROTARJETAVISIBLE = {} \
                                WHERE idsite = {} \
                                AND idmediopago = {}"
                                 .format(cardNumberFormat, siteId, paymentMethodId))

    replicate(siteId)

def getCardNumberFormat(siteId, paymentMethodId):
    cardNumberFormat = DBConnection.query("SELECT FORMATONROTARJETAVISIBLE  \
                                    FROM sps433.spsmedpagotienda \
                                    WHERE idsite = {} \
                                    AND idmediopago = {}"
                       .format(siteId, paymentMethodId))

    return cardNumberFormat