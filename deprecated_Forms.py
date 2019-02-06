from settings import *
from Exceptions import URLStatusCodeNot200Exception
import os
import requests

formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]

def encryptTxId(aliasKey, vep):
    response = requests.get(("http://{}:{}/sign/{}/{}").format(formsBaseURL, formsPort, aliasKey, vep))
    if response.ok:
        return (response.json()["encrypt"])

def validateAFIP(vep, encryptedTxId, site, email="juan.rego@redb.ee", redirectUrl="http://www.redbee.io/"):
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
    else:
        raise URLStatusCodeNot200Exception("Received response has not been OK. Details: \n"
                                           #"Headers sent: \n {}\n"
                                           #"Request sent: \n {}\n"
                                           "Response received: \n {}:{}\n".format(headers,json,response,response.text))

