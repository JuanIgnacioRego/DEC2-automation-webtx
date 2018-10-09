# -*- coding: utf-8 -*-
import time
import os

compraSimpleMandatoryFields = [
    "NROCOMERCIO",
    "NROOPERACION",
    "MONTO",
    "CUOTAS",
    "MONEDA",
    "MEDIODEPAGO",
]

"""
Default expiration time: 30 mins.
Configurable on DB (for a specific site) on spssites.timeoutcompra. 
Configurable on Marathon via environment variable 'FORM_TIMEOUT_SECONDS' (for all sites, in seconds).

"""
lifetime_Forms = 220
# -- VISA --
validationVisa = {
    "NOMBREENTARJETA" : "HOMERO JAY SIMPSON",
    "NROTARJETA" : "4509790113276723",#4242424242424242 #4509790112684851 #4509790112684851
    "idComboMes" : "12",
    "idComboAno" : "20",
    "CODSEGURIDAD" : "123",
    "EMAILCLIENTE" : "hj@simpson.com",
    "TIPODOC" : "1",
    "NRODOC" : "11222333",
    "CALLE" : "Av. Siempre Viva",
    "NROPUERTA" : "0",
    "FECHANACIMIENTO" : "01011990"
}

compraSimpleVisa = {
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "VISA " + str(int(time.time())),
    "MONTO": "20000",
    "CUOTAS": "12",
    "MONEDA": "1",
    "MEDIODEPAGO": "1",
    #"URLDINAMICA": "http://request-bin:1529/t31qr0t3"
    #"URLDINAMICA": "http://marathon-lb.infrastructure.marathon.mesos:10113/sxusbesx" this works!
    "URLDINAMICA": os.getenv("PPBLINK")
}

validationVisa_AFIP = {
    "NOMBREENTARJETA" : "Una Persona Fiscal",
    "NROTARJETA" : "4509790113276723",#4242424242424242 #4509790112684851 #4509790112684851
    "idComboMes" : "12",
    "idComboAno" : "20",
    "CODSEGURIDAD" : "123",
    "EMAILCLIENTE" : "juan.rego@redb.ee"
}
txSimpleVisa_AFIP ={
    "NROCOMERCIO": "03101980",
    "NROOPERACION": str(int(time.time())),
}

compraDistribuidaVisa = {
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "VISA_Distribuida " + str(int(time.time())),
    "MONTO": "30000",
    "CUOTAS": "1",
    "MONEDA": "1",
    "MEDIODEPAGO": "1",
    "IDMODALIDAD" : "S",
    "SITEDIST":"28464384#28464385#28464386",
    "CUOTASDIST":"1#1#1",
    "IMPDIST":"10000#10000#10000"
}

# -- MASTERCARD --
compraSimpleMastercard = {
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "MASTER " + str(int(time.time())),
    "MONTO": "30000",
    "CUOTAS": "3",
    "MONEDA": "1",
    "MEDIODEPAGO": "15"
}

compraDistribuidaMastercard ={
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "MASTER_D " + str(int(time.time())),
    "MONTO": "100",
    "CUOTAS": "1",
    "MONEDA": "1",
    "MEDIODEPAGO": "15",
    "IDMODALIDAD" : "S", # "" means "Default", and that means "NO Distribuida"
    "SITEDIST":"28464384#28464385#28464386",
    "CUOTASDIST":"1#1",
    "IMPDIST":"50#50"
}

validationMastercard = {
    "NOMBREENTARJETA" : "I'm Mr. Mastercard",
    "NROTARJETA" : "5323622277777785",
    "VENCTARJETA" : "1220",
    "CODSEGURIDAD" : "268",
    "EMAILCLIENTE" : "automation@mastercard.com.ar"
}

# -- NATIVA VISA --
validationNativaVisa = {
    "NOMBREENTARJETA" : "Pepe Argento",
    "NROTARJETA" : "4870173852824121",
    "VENCTARJETA" : "1220",
    "CODSEGURIDAD" : "123",
    "EMAILCLIENTE" : "pepeargento2006@jotmail.com",
    "TIPODOC" : "1",
    "NRODOC" : "11222333",
    "CALLE" : "Alguna Calle en Flores",
    "NROPUERTA" : "5000",
    "FECHANACIMIENTO" : "01011990"
}

compraSimpleNativaVisa = {
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "NATIVA VISA " + str(int(time.time())),
    "MONTO": "2000",
    "CUOTAS": "12",
    "MONEDA": "1",
    "MEDIODEPAGO": "42"
}


# -- NATIVA MASTERCARD --

validationNativaMastercard = {
    "NOMBREENTARJETA" : "Moni Argento",
    "NROTARJETA" : "5465539992525000",
    "VENCTARJETA" : "1221",
    "CODSEGURIDAD" : "711",
    "EMAILCLIENTE" : "moniargento2008@jotmail.com",
    "TIPODOC" : "1",
    "NRODOC" : "11222333",
    "CALLE" : "Alguna Calle en Flores",
    "NROPUERTA" : "5000",
    "FECHANACIMIENTO" : "01011990"
}

compraSimpleNativaMastercard = {
    "NROCOMERCIO": "28464383",
    "NROOPERACION": "NATIVA MASTERCARD " + str(int(time.time())),
    "MONTO": "2000",
    "CUOTAS": "12",
    "MONEDA": "1",
    "MEDIODEPAGO": "42"
}

compraSimpleConAgregador ={
"aindicador" : "",
"adocumento" : "20380940060",
"afactpagar" : "mnbvcxasmg",
"afactdevol" : "12345678902",
"anombrecom" : "leila / di /ciocco12",
"adomiciliocomercio" : "calle 123 lavalle 1",
"anropuerta" : "123456",
"acodpostal" : "1234567",
"arubro" : "1234",
"acodcanal" : "1k0",
"acodgeografico" : "12345",
"NROCOMERCIO": "28464383",
"NROOPERACION": "VISA " + str(int(time.time())),
"MONTO": "2000",
"CUOTAS": "12",
"MONEDA": "1",
"MEDIODEPAGO": "1"
   
}

# -- FAILED CARDS! --
validationVisa_ExpiredCard = validationVisa.copy()
validationVisa_ExpiredCard ["idComboAno"] = "15"

vepExample = {

    "card_number" : "4507990000004905",

    "user_cuit": "20240215455",

    "number_vep": "000292454419",

    "cp": {

           "posting_date": "2017-03-21",

           "transaction_id": "862637468273",

           "payment_entity": "1002",

           "payer_bank": "389",

           "nro_ticket":"3839",

           "control_code": "005248",

           "payment_format": "1",

           "payment_datetime": "2017-03-21 10:23:57",

           "payment_form": "1",

           "branch_office_type": 8,

           "taxpayer": "20240215455",

           "currency": "1",

           "amount": "1186.30"
     }

}