# -*- coding: utf-8 -*-
import time
import os

# VARIABLES DE ENTORNO

forms_env = {
    "ALIAS_KEY":"redbee",
    "AFIP_SITE_ID":"03101980"
}



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
    "FECHANACIMIENTO" : "01011990",
    "FECHAVTO":"1220"
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
    "NROTARJETA" : "4509790112684851",#"4509790113276723",#4242424242424242 #4509790112684851 #4509790112684851
    "idComboMes" : "03",
    "idComboAno" : "19",
    "CODSEGURIDAD" : "879",
    "EMAILCLIENTE" : "juan.rego@redb.ee",
    "NRODOC":"" #debe estar vacío
}
txSimpleVisa_AFIP ={
    "NROCOMERCIO": "03101980",
    "NROOPERACION": str(int(time.time())),
    "MONTO": "3000000", #equivale a $30.000, extraído del VEP
    #En realidad, el monto se encuentra definido en el VEP, en el campo "amount". El valor es tal cual
    #se define en "amount", es decir, "amount":"30000" equivale a $30.000 (a diferencia de RestTx, donde
    #se toman los dos últimos números como centavos.
    "CUOTAS": "1",
    "MONEDA": "1",
    "MEDIODEPAGO": "1",
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
validationVisa_Rejected = validationVisa.copy()
validationVisa_Rejected ["NROTARJETA"] = "4242424242424242"

validationVisa_ExpiredCard = validationVisa.copy()
validationVisa_ExpiredCard ["idComboAno"] = "15"

# FONDOS INSUFICIENTES
validationVisa_Rejected_51 = validationVisa.copy()
validationVisa_Rejected_51["NROTARJETA"] = "-"
validationVisa_Rejected_51["brandMessage"] = "FONDOS INSUFICIENTES"

# TARJETA VENCIDA
validationVisa_Rejected_54 = validationVisa.copy()
validationVisa_Rejected_54["NROTARJETA"] = "4509790161212018"
validationVisa_Rejected_54["brandMessage"] = "TARJETA VENCIDA"

# DENEGADA
validationVisa_Rejected_05 = validationVisa.copy()
validationVisa_Rejected_05["NROTARJETA"] = "4508152005527096"
validationVisa_Rejected_05["brandMessage"] = "DENEGADA"

# COMERCIO INVALIDO
validationVisa_Rejected_03 = validationVisa.copy()
validationVisa_Rejected_03["NROTARJETA"] = "4555990015629952"
validationVisa_Rejected_03["brandMessage"] = "COMERCIO INVALIDO"

# CAPTURAR TARJETA
validationVisa_Rejected_04 = validationVisa.copy()
validationVisa_Rejected_04["NROTARJETA"] = "4548503001949522"
validationVisa_Rejected_04["brandMessage"] = "CAPTURAR TARJETA"

# PEDIR AUTORIZACION
validationVisa_Rejected_01 = validationVisa.copy()
validationVisa_Rejected_01["NROTARJETA"] = "4507910000000018"
validationVisa_Rejected_01["brandMessage"] = "PEDIR AUTORIZACION"

# RETENGA Y LLAME
validationVisa_Rejected_07 = validationVisa.copy()
validationVisa_Rejected_07["NROTARJETA"] = "4509950077820030"
validationVisa_Rejected_07["brandMessage"] = "RETENGA Y LLAME"

# LLAMAR AL EMISOR
validationVisa_Rejected_76 = validationVisa.copy()
validationVisa_Rejected_76["NROTARJETA"] = "4509950077820040"
validationVisa_Rejected_76["brandMessage"] = "LLAMAR AL EMISOR"

# RETENER TARJETA
validationVisa_Rejected_43 = validationVisa.copy()
validationVisa_Rejected_43["NROTARJETA"] = "4831540009057581"
validationVisa_Rejected_43["brandMessage"] = "RETENER TARJETA"

# EMISOR FUERA LINEA
validationVisa_Rejected_91 = validationVisa.copy()
validationVisa_Rejected_91["NROTARJETA"] = "4509950077820043"
validationVisa_Rejected_91["brandMessage"] = "EMISOR FUERA LINEA"

# ERROR EN SISTEMA
validationVisa_Rejected_96 = validationVisa.copy()
validationVisa_Rejected_96["NROTARJETA"] = "45099500778200346"
validationVisa_Rejected_96["brandMessage"] = "ERROR EN SISTEMA"

# TRANSAC. INVALIDA
validationVisa_Rejected_12 = validationVisa.copy()
validationVisa_Rejected_12["NROTARJETA"] = "4509790065807160"
validationVisa_Rejected_12["brandMessage"] = "TRANSAC. INVALIDA"

# EXCEDE MAX. CUOTAS
validationVisa_Rejected_48 = validationVisa.copy()
validationVisa_Rejected_48["NROTARJETA"] = "4509950077820034"
validationVisa_Rejected_48["brandMessage"] = "EXCEDE MAX. CUOTAS"

# TARJETA VENCIDA
validationVisa_Rejected_54 = validationVisa.copy()
validationVisa_Rejected_54["NROTARJETA"] = "4509950077820037"
validationVisa_Rejected_54["brandMessage"] = "TARJETA VENCIDA"

# TARJ. NO HABILITADA
validationVisa_Rejected_56 = validationVisa.copy()
validationVisa_Rejected_56["NROTARJETA"] = "4509950120462696"
validationVisa_Rejected_56["brandMessage"] = "TARJ. NO HABILITADA"

# MONTO INVALIDO
validationVisa_Rejected_13 = validationVisa.copy()
validationVisa_Rejected_13["NROTARJETA"] = "4509950077820031"
validationVisa_Rejected_13["brandMessage"] = "MONTO INVALIDO"


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

