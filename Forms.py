from settings import *
import os
import requests

formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]

def encryptTxId(aliasKey, vep):
    response = requests.get(("http://{}:{}/sign/{}/{}").format(formsBaseURL, formsPort, aliasKey, vep))
    if response.ok:
        return (response.json()["encrypt"])

def validateAFIP(vep, encryptedTxId, site, email="juan.rego@redb.ee", redirectUrl="http://www.afip.gob.ar/sitio/externos/default.asp"):
    headers = {"X-Consumer-Username": "{}_pci".format(site)}
    json = {
        "transaction_id": vep,
        "signed_transaction_id": encryptedTxId,
        "customer": {
            "email": email
        },
        "redirect_url": redirectUrl,
        "vep": {
            "number": vep
        }
    }
    response = requests.post(("http://{}:{}/form/afip").format(formsBaseURL,formsPort),
                             headers = headers,
                             json = json)
    if response.ok:
        return (response.text)

