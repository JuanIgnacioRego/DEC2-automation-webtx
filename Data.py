# -*- coding: utf-8 -*-
import time
import os

# VARIABLES DE ENTORNO

forms_env = {
    "ALIAS_KEY":"redbee",
    "AFIP_SITE_ID":"03101980"
}

CyberSource = {
    "securityKey":"0fbmBP/Jr4IDbz+Qx6nOk4cWZSnD5iXb9w4Rkp1vQrFSWKKAQRoDF1Tls9mFGplPC4vmDMY1IcrUrlwb4bM+KGheF/97J4RXqjFOi7UQZg33WsAYX4nrxsloka+OdSa6ewxlEaJ1yYhg4T5rGIcKef2wzUddqqxxqr/B7wavz8ycNZ5uwQZdd8e2or9qzsstWOhNpcILOmF3t+2N8Px+6/jUAiK8JqhJBPnPqMmRAEXZnmZWcuWB4i4Pq1WAdjrgb4u0Qa4sITe8yPRZtoD59oE1h83ywc8CmkJxL9dDzjv4RZkmanDrKNGv6s9Jws9phdtT6i56XpnROADB96AC1A==",
    "verticales":{
        "DigitalGoods":1,
        "Retail":2,
        "Services":3,
        "Ticketing":4,
        "Travel":5,
        "RetailTP":6
    }
}

sites = {
    "Swatch":"28464383"
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
    "NROTARJETA" : "4509790112684851",#4242424242424242 #4509790112684851
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
    "NROOPERACION": "VISA " + str(int(time.time())),
    "NROCOMERCIO": "28464383",
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
    "MEDIODEPAGO": "42",
    "URLDINAMICA": os.getenv("PPBLINK")
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

validationData_Swatch_CS_DigitalGoods  = {
     "site": {
         "transaction_id": "Swatch CS DigitalGoods {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/",
    "fraud_detection": {
        "send_to_cs": True,
        "channel": "Web/Mobile/Telefonica",
        "bill_to": {
            "city": "Buenos Aires",
            "country": "AR",
            "customer_id": "martinid",
            "email": "accept@decidir.com.ar",
            "first_name": "martin",
            "last_name": "paoletta",
            "phone_number": "1547766329",
            "postal_code": "1427",
            "state": "BA",
            "street1": "GARCIA DEL RIO 4041",
            "street2": "GARCIA DEL RIO 4041"
        },
        "purchase_totals": {
            "currency": "ARS",
            "amount": 2
        },
        "customer_in_site": {
            "days_in_site": 243,
            "is_guest": False,
            "password": "abracadabra",
            "num_of_transactions": 1,
            "cellphone_number": "12121",
            "date_of_birth": "129412",
            "street": "RIO 4041"
        },
        "device_unique_id": "12345",
        "digital_goods_transaction_data": {
            "delivery_type": "Pick up",
            "items": [
                {
                    "code": "popblacksabbat2016",
                    "description": "Popular Black Sabbath 2016",
                    "name": "popblacksabbat2016ss",
                    "sku": "asas",
                    "total_amount": 20,
                    "quantity": 1,
                    "unit_price": 20
                },
                {
                    "code": "popblacksabbat2016",
                    "description": "Popular Black Sabbath 2016",
                    "name": "popblacksabbat2016ss",
                    "sku": "asas",
                    "total_amount": 20,
                    "quantity": 1,
                    "unit_price": 20
                }
            ]
        },

        "csmdds": [
            {"code": 17, "description": "Campo MDD17"},
            {"code": 18, "description": "Campo MDD18"},
            {"code": 19, "description": "Campo MDD19"},
            {"code": 20, "description": "Campo MDD20"},
            {"code": 21, "description": "Campo MDD21"},
            {"code": 22, "description": "Campo MDD22"},
            {"code": 23, "description": "Campo MDD23"},
            {"code": 24, "description": "Campo MDD24"},
            {"code": 25, "description": "Campo MDD25"},
            {"code": 26, "description": "Campo MDD26"},
            {"code": 27, "description": "Campo MDD27"},
            {"code": 28, "description": "Campo MDD28"},
            {"code": 29, "description": "Campo MDD29"},
            {"code": 30, "description": "Campo MDD30"},
            {"code": 31, "description": "Campo MDD31"},
            {"code": 33, "description": "Campo MDD33"},
            {"code": 34, "description": "Campo MDD34"},
            {"code": 43, "description": "Campo MDD43"},
            {"code": 44, "description": "Campo MDD44"},
            {"code": 45, "description": "Campo MDD45"},
            {"code": 46, "description": "Campo MDD46"},
            {"code": 47, "description": "Campo MDD47"},
            {"code": 48, "description": "Campo MDD48"},
            {"code": 49, "description": "Campo MDD49"},
            {"code": 50, "description": "Campo MDD50"},
            {"code": 51, "description": "Campo MDD51"},
            {"code": 52, "description": "Campo MDD52"},
            {"code": 53, "description": "Campo MDD53"},
            {"code": 54, "description": "Campo MDD54"},
            {"code": 55, "description": "Campo MDD55"},
            {"code": 56, "description": "Campo MDD56"},
            {"code": 57, "description": "Campo MDD57"},
            {"code": 58, "description": "Campo MDD58"},
            {"code": 59, "description": "Campo MDD59"},
            {"code": 60, "description": "Campo MDD60"},
            {"code": 61, "description": "Campo MDD61"},
            {"code": 62, "description": "Campo MDD62"},
            {"code": 63, "description": "Campo MDD63"},
            {"code": 64, "description": "Campo MDD64"},
            {"code": 65, "description": "Campo MDD65"},
            {"code": 66, "description": "Campo MDD66"},
            {"code": 67, "description": "Campo MDD67"},
            {"code": 68, "description": "Campo MDD68"},
            {"code": 69, "description": "Campo MDD69"},
            {"code": 70, "description": "Campo MDD70"},
            {"code": 71, "description": "Campo MDD71"},
            {"code": 72, "description": "Campo MDD72"},
            {"code": 73, "description": "Campo MDD73"},
            {"code": 74, "description": "Campo MDD74"},
            {"code": 75, "description": "Campo MDD75"},
            {"code": 76, "description": "Campo MDD76"},
            {"code": 77, "description": "Campo MDD77"},
            {"code": 78, "description": "Campo MDD78"},
            {"code": 79, "description": "Campo MDD79"},
            {"code": 80, "description": "Campo MDD80"},
            {"code": 81, "description": "Campo MDD81"},
            {"code": 82, "description": "Campo MDD82"},
            {"code": 83, "description": "Campo MDD83"},
            {"code": 84, "description": "Campo MDD84"},
            {"code": 85, "description": "Campo MDD85"},
            {"code": 86, "description": "Campo MDD86"},
            {"code": 87, "description": "Campo MDD87"},
            {"code": 88, "description": "Campo MDD88"},
            {"code": 89, "description": "Campo MDD89"},
            {"code": 90, "description": "Campo MDD90"},
            {"code": 91, "description": "Campo MDD91"},
            {"code": 92, "description": "Campo MDD92"},
            {"code": 93, "description": "Campo MDD93"},
            {"code": 94, "description": "Campo MDD94"},
            {"code": 95, "description": "Campo MDD95"},
            {"code": 96, "description": "Campo MDD96"},
            {"code": 97, "description": "Campo MDD97"},
            {"code": 98, "description": "Campo MDD98"},
            {"code": 99, "description": "Campo MDD99"}
        ]
    }
 }

validationData_Swatch_CS_Retail  = {
     "site": {
         "transaction_id": "Swatch CS Retail {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "fraud_detection": {
      "send_to_cs": True,
      "channel": "Web/Mobile/Telefonica",
      "bill_to": {
        "city": "Buenos Aires",
         "country": "AR",
         "customer_id": "martinid",
         "email": "accept@decidir.com.ar",
         "first_name": "martin",
         "last_name": "paoletta",
         "phone_number": "1547766329",
         "postal_code": "1427",
         "state": "BA",
         "street1": "GARCIA DEL RIO 4041",
         "street2": "GARCIA DEL RIO 4041"
      },
      "purchase_totals": {
         "currency": "ARS",
         "amount": 2
      },
      "customer_in_site": {
         "days_in_site": 243,
         "is_guest": False,
         "password": "abracadabra",
         "num_of_transactions": 1,
         "cellphone_number": "12121",
         "date_of_birth": "129412",
         "street": "RIO 4041"
      },
      "retail_transaction_data": {
         "ship_to": {
            "city": "Buenos Aires",
            "country": "AR",
            "email": "accept@decidir.com.ar",
            "first_name": "martin",
            "last_name": "paoletta",
            "phone_number": "1547766329",
            "postal_code": "1427",
            "state": "BA",
            "street1": "GARCIA DEL RIO 4041",
            "street2": "GARCIA DEL RIO 4041"
      },
         "days_to_delivery": "55",
         "dispatch_method": "storepickup",
         "tax_voucher_required": True,
         "customer_loyality_number": "123232",
         "coupon_code": "cupon22",
         "items": [
            {
               "code": "popblacksabbat2016",
               "description": "Popular Black Sabbath 2016",
               "name": "popblacksabbat2016ss",
               "sku": "asas",
               "total_amount": 20,
               "quantity": 1,
               "unit_price": 20
            },
           {
              "code": "popblacksdssabbat2016",
              "description": "Popular Blasdsck Sabbath 2016",
              "name": "popblacksabbatdsds2016ss",
              "sku": "aswewas",
              "total_amount": 111212,
              "quantity": 1,
              "unit_price": 111212
           }
         ]
      },
        "csmdds": [
         {"code": 17, "description": "Campo MDD17"},
          {"code": 18, "description": "Campo MDD18"},
         {"code": 19, "description": "Campo MDD19"},
         {"code": 20, "description": "Campo MDD20"},
         {"code": 21, "description": "Campo MDD21"},
         {"code": 22, "description": "Campo MDD22"},
         {"code": 23, "description": "Campo MDD23"},
         {"code": 24, "description": "Campo MDD24"},
         {"code": 25, "description": "Campo MDD25"},
         {"code": 26, "description": "Campo MDD26"},
         {"code": 27, "description": "Campo MDD27"},
         {"code": 28, "description": "Campo MDD28"},
         {"code": 29, "description": "Campo MDD29"},
         {"code": 30, "description": "Campo MDD30"},
         {"code": 31, "description": "Campo MDD31"},
         {"code": 32, "description": "Campo MDD32"},
         {"code": 33, "description": "Campo MDD33"},
         {"code": 34, "description": "Campo MDD34"},
         {"code": 43, "description": "Campo MDD43"},
         {"code": 44, "description": "Campo MDD44"},
         {"code": 45, "description": "Campo MDD45"},
         {"code": 46, "description": "Campo MDD46"},
         {"code": 47, "description": "Campo MDD47"},
         {"code": 48, "description": "Campo MDD48"},
         {"code": 49, "description": "Campo MDD49"},
         {"code": 50, "description": "Campo MDD50"},
         {"code": 51, "description": "Campo MDD51"},
         {"code": 52, "description": "Campo MDD52"},
         {"code": 53, "description": "Campo MDD53"},
         {"code": 54, "description": "Campo MDD54"},
         {"code": 55, "description": "Campo MDD55"},
         {"code": 56, "description": "Campo MDD56"},
         {"code": 57, "description": "Campo MDD57"},
         {"code": 58, "description": "Campo MDD58"},
         {"code": 59, "description": "Campo MDD59"},
         {"code": 60, "description": "Campo MDD60"},
         {"code": 61, "description": "Campo MDD61"},
         {"code": 62, "description": "Campo MDD62"},
         {"code": 63, "description": "Campo MDD63"},
         {"code": 64, "description": "Campo MDD64"},
         {"code": 65, "description": "Campo MDD65"},
         {"code": 66, "description": "Campo MDD66"},
         {"code": 67, "description": "Campo MDD67"},
         {"code": 68, "description": "Campo MDD68"},
         {"code": 69, "description": "Campo MDD69"},
         {"code": 70, "description": "Campo MDD70"},
         {"code": 71, "description": "Campo MDD71"},
         {"code": 72, "description": "Campo MDD72"},
         {"code": 73, "description": "Campo MDD73"},
         {"code": 74, "description": "Campo MDD74"},
         {"code": 75, "description": "Campo MDD75"},
         {"code": 76, "description": "Campo MDD76"},
         {"code": 77, "description": "Campo MDD77"},
         {"code": 78, "description": "Campo MDD78"},
         {"code": 79, "description": "Campo MDD79"},
         {"code": 80, "description": "Campo MDD80"},
         {"code": 81, "description": "Campo MDD81"},
         {"code": 82, "description": "Campo MDD82"},
         {"code": 83, "description": "Campo MDD83"},
         {"code": 84, "description": "Campo MDD84"},
         {"code": 85, "description": "Campo MDD85"},
         {"code": 86, "description": "Campo MDD86"},
         {"code": 87, "description": "Campo MDD87"},
         {"code": 88, "description": "Campo MDD88"},
         {"code": 89, "description": "Campo MDD89"},
         {"code": 90, "description": "Campo MDD90"},
         {"code": 91, "description": "Campo MDD91"},
         {"code": 92, "description": "Campo MDD92"},
         {"code": 93, "description": "Campo MDD93"},
         {"code": 94, "description": "Campo MDD94"},
         {"code": 95, "description": "Campo MDD95"},
         {"code": 96, "description": "Campo MDD96"},
         {"code": 97, "description": "Campo MDD97"},
         {"code": 98, "description": "Campo MDD98"},
         {"code": 99, "description": "Campo MDD99"}
      ]
   },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/"
 }

validationData_Swatch_CS_Services  = {
     "site": {
         "transaction_id": "Swatch CS Services {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/",
"fraud_detection": {
      "send_to_cs": True,
      "channel": "Web/Mobile/Telefonica",
      "bill_to": {
        "city": "Buenos Aires",
         "country": "AR",
         "customer_id": "martinid",
         "email": "accept@decidir.com.ar",
         "first_name": "martin",
         "last_name": "paoletta",
         "phone_number": "1547766329",
         "postal_code": "1427",
         "state": "BA",
         "street1": "GARCIA DEL RIO 4041",
         "street2": "GARCIA DEL RIO 4041"
      },
      "purchase_totals": {
         "currency": "ARS",
         "amount": 2
      },
      "customer_in_site": {
         "days_in_site": 243,
         "is_guest": False,
         "password": "abracadabra",
         "num_of_transactions": 1,
         "cellphone_number": "12121",
         "date_of_birth": "129412",
         "street": "RIO 4041"
      },
      "services_transaction_data": {
      	  "service_type": "eltipodelservicio",
      	  "reference_payment_service1": "reference1",
         "reference_payment_service2": "reference2",
         "reference_payment_service3": "reference3",

         "items": [
            {
               "code": "popblacksabbat2016",
               "description": "Popular Black Sabbath 2016",
               "name": "popblacksabbat2016ss",
               "sku": "asas",
               "total_amount": 20,
               "quantity": 1,
               "unit_price": 20
            },
           {
              "code": "popblacksdssabbat2016",
              "description": "Popular Blasdsck Sabbath 2016",
              "name": "popblacksabbatdsds2016ss",
              "sku": "aswewas",
              "total_amount": 111212,
              "quantity": 1,
              "unit_price": 111212
           }
         ]
      },
        "csmdds": [
         {"code": 17, "description": "Campo MDD17"},
         {"code": 18, "description": "Campo MDD18"},
         {"code": 19, "description": "Campo MDD19"},
         {"code": 20, "description": "Campo MDD20"},
         {"code": 21, "description": "Campo MDD21"},
         {"code": 22, "description": "Campo MDD22"},
         {"code": 23, "description": "Campo MDD23"},
         {"code": 24, "description": "Campo MDD24"},
         {"code": 25, "description": "Campo MDD25"},
         {"code": 26, "description": "Campo MDD26"},
         {"code": 27, "description": "Campo MDD27"},
         {"code": 28, "description": "Campo MDD28"},
         {"code": 29, "description": "Campo MDD29"},
         {"code": 30, "description": "Campo MDD30"},
         {"code": 31, "description": "Campo MDD31"},
         {"code": 32, "description": "Campo MDD32"},
         {"code": 33, "description": "Campo MDD33"},
         {"code": 34, "description": "Campo MDD34"},
         {"code": 43, "description": "Campo MDD43"},
         {"code": 44, "description": "Campo MDD44"},
         {"code": 45, "description": "Campo MDD45"},
         {"code": 46, "description": "Campo MDD46"},
         {"code": 47, "description": "Campo MDD47"},
         {"code": 48, "description": "Campo MDD48"},
         {"code": 49, "description": "Campo MDD49"},
         {"code": 50, "description": "Campo MDD50"},
         {"code": 51, "description": "Campo MDD51"},
         {"code": 52, "description": "Campo MDD52"},
         {"code": 53, "description": "Campo MDD53"},
         {"code": 54, "description": "Campo MDD54"},
         {"code": 55, "description": "Campo MDD55"},
         {"code": 56, "description": "Campo MDD56"},
         {"code": 57, "description": "Campo MDD57"},
         {"code": 58, "description": "Campo MDD58"},
         {"code": 59, "description": "Campo MDD59"},
         {"code": 60, "description": "Campo MDD60"},
         {"code": 61, "description": "Campo MDD61"},
       {"code": 62, "description": "Campo MDD62"},
         {"code": 63, "description": "Campo MDD63"},
         {"code": 64, "description": "Campo MDD64"},
         {"code": 65, "description": "Campo MDD65"},
         {"code": 66, "description": "Campo MDD66"},
         {"code": 67, "description": "Campo MDD67"},
         {"code": 68, "description": "Campo MDD68"},
         {"code": 69, "description": "Campo MDD69"},
         {"code": 70, "description": "Campo MDD70"},
         {"code": 71, "description": "Campo MDD71"},
         {"code": 72, "description": "Campo MDD72"},
         {"code": 73, "description": "Campo MDD73"},
         {"code": 74, "description": "Campo MDD74"},
         {"code": 75, "description": "Campo MDD75"},
         {"code": 76, "description": "Campo MDD76"},
         {"code": 77, "description": "Campo MDD77"},
         {"code": 78, "description": "Campo MDD78"},
         {"code": 79, "description": "Campo MDD79"},
         {"code": 80, "description": "Campo MDD80"},
         {"code": 81, "description": "Campo MDD81"},
         {"code": 82, "description": "Campo MDD82"},
         {"code": 83, "description": "Campo MDD83"},
         {"code": 84, "description": "Campo MDD84"},
         {"code": 85, "description": "Campo MDD85"},
         {"code": 86, "description": "Campo MDD86"},
         {"code": 87, "description": "Campo MDD87"},
         {"code": 88, "description": "Campo MDD88"},
         {"code": 89, "description": "Campo MDD89"},
         {"code": 90, "description": "Campo MDD90"},
         {"code": 91, "description": "Campo MDD91"},
         {"code": 92, "description": "Campo MDD92"},
         {"code": 93, "description": "Campo MDD93"},
         {"code": 94, "description": "Campo MDD94"},
         {"code": 95, "description": "Campo MDD95"},
         {"code": 96, "description": "Campo MDD96"},
         {"code": 97, "description": "Campo MDD97"},
         {"code": 98, "description": "Campo MDD98"},
         {"code": 99, "description": "Campo MDD99"}
      ]
   }
 }

validationData_Swatch_CS_Ticketing  = {
     "site": {
         "transaction_id": "Swatch CS Ticketing {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/",
"fraud_detection": {
        "send_to_cs": True,
        "channel": "Web/Mobile/Telefonica",
        "bill_to": {
        "city": "Buenos Aires",
        "country": "AR",
        "customer_id": "martinid",
        "email": "accept@decidir.com.ar",
        "first_name": "leila",
      "last_name": "PPP",
        "phone_number": "2322323232",
        "postal_code": "1223",
        "state": "BA",
        "street1": "Italia 1234",
        "street2": "Italia 1234"
     },
        "purchase_totals": {
        "currency": "ARS",
        "amount": 12444
     },
     "customer_in_site": {
        "days_in_site": 243,
        "is_guest": False,
        "password": "abracadabra",
        "num_of_transactions": 1,
        "cellphone_number": "12121",
        "date_of_birth": "129412",
        "street": "RIO 4041"
     },
     "ticketing_transaction_data": {
        "days_to_event": 55,
        "delivery_type": "Pick up",
        "items": [
           {
              "code": "popblacksabbat2016",
              "description": "Popular Black Sabbath 2016",
              "name": "popblacksabbat2016ss",
              "sku": "asas",
              "total_amount": 242424,
              "quantity": 2,
              "unit_price": 121212
           },
           {
              "code": "popblacksdssabbat2016",
              "description": "Popular Blasdsck Sabbath 2016",
              "name": "popblacksabbatdsds2016ss",
              "sku": "aswewas",
              "total_amount": 111212,
              "quantity": 1,
              "unit_price": 111212
           }
        ]
     },
        "csmdds": [
         {"code": 12, "description": "Campo MDD12"},
         {"code": 14, "description": "Campo MDD14"},
         {"code": 15, "description": "Campo MDD15"},
         {"code": 16, "description": "Campo MDD16"},
         {"code": 17, "description": "Campo MDD17"},
         {"code": 18, "description": "Campo MDD18"},
         {"code": 19, "description": "Campo MDD19"},
         {"code": 20, "description": "Campo MDD20"},
         {"code": 21, "description": "Campo MDD21"},
         {"code": 22, "description": "Campo MDD22"},
         {"code": 23, "description": "Campo MDD23"},
         {"code": 24, "description": "Campo MDD24"},
         {"code": 25, "description": "Campo MDD25"},
         {"code": 26, "description": "Campo MDD26"},
         {"code": 27, "description": "Campo MDD27"},
         {"code": 28, "description": "Campo MDD28"},
         {"code": 29, "description": "Campo MDD29"},
         {"code": 30, "description": "Campo MDD30"},
         {"code": 31, "description": "Campo MDD31"},
         {"code": 32, "description": "Campo MDD32"},
         {"code": 43, "description": "Campo MDD43"},
         {"code": 44, "description": "Campo MDD44"},
         {"code": 45, "description": "Campo MDD45"},
         {"code": 46, "description": "Campo MDD46"},
         {"code": 47, "description": "Campo MDD47"},
         {"code": 48, "description": "Campo MDD48"},
         {"code": 49, "description": "Campo MDD49"},
         {"code": 50, "description": "Campo MDD50"},
         {"code": 51, "description": "Campo MDD51"},
         {"code": 52, "description": "Campo MDD52"},
         {"code": 53, "description": "Campo MDD53"},
         {"code": 54, "description": "Campo MDD54"},
         {"code": 55, "description": "Campo MDD55"},
         {"code": 56, "description": "Campo MDD56"},
         {"code": 57, "description": "Campo MDD57"},
         {"code": 58, "description": "Campo MDD58"},
         {"code": 59, "description": "Campo MDD59"},
         {"code": 60, "description": "Campo MDD60"},
         {"code": 61, "description": "Campo MDD61"},
         {"code": 62, "description": "Campo MDD62"},
         {"code": 63, "description": "Campo MDD63"},
         {"code": 64, "description": "Campo MDD64"},
         {"code": 65, "description": "Campo MDD65"},
         {"code": 66, "description": "Campo MDD66"},
         {"code": 67, "description": "Campo MDD67"},
         {"code": 68, "description": "Campo MDD68"},
         {"code": 69, "description": "Campo MDD69"},
         {"code": 70, "description": "Campo MDD70"},
         {"code": 71, "description": "Campo MDD71"},
         {"code": 72, "description": "Campo MDD72"},
         {"code": 73, "description": "Campo MDD73"},
         {"code": 74, "description": "Campo MDD74"},
         {"code": 75, "description": "Campo MDD75"},
         {"code": 76, "description": "Campo MDD76"},
         {"code": 77, "description": "Campo MDD77"},
         {"code": 78, "description": "Campo MDD78"},
         {"code": 79, "description": "Campo MDD79"},
         {"code": 80, "description": "Campo MDD80"},
         {"code": 81, "description": "Campo MDD81"},
         {"code": 82, "description": "Campo MDD82"},
         {"code": 83, "description": "Campo MDD83"},
         {"code": 84, "description": "Campo MDD84"},
         {"code": 85, "description": "Campo MDD85"},
         {"code": 86, "description": "Campo MDD86"},
         {"code": 87, "description": "Campo MDD87"},
         {"code": 88, "description": "Campo MDD88"},
         {"code": 89, "description": "Campo MDD89"},
         {"code": 90, "description": "Campo MDD90"},
         {"code": 91, "description": "Campo MDD91"},
         {"code": 92, "description": "Campo MDD92"},
         {"code": 93, "description": "Campo MDD93"},
         {"code": 94, "description": "Campo MDD94"},
         {"code": 95, "description": "Campo MDD95"},
         {"code": 96, "description": "Campo MDD96"},
         {"code": 97, "description": "Campo MDD97"},
         {"code": 98, "description": "Campo MDD98"},
         {"code": 99, "description": "Campo MDD99"}
      ]
  }

 }

validationData_Swatch_CS_Travel  = {
     "site": {
         "transaction_id": "Swatch CS Travel {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/",
"fraud_detection": {
        "send_to_cs": True,
      "bill_to": {
         "city": "Buenos Aires",
         "country": "AR",
         "customer_id": "martinid",
         "email": "accept@decidir.com.ar",
         "first_name": "martin",
         "last_name": "paoletta",
         "phone_number": "1547766329",
         "postal_code": "1427",
         "state": "BA",
         "street1": "GARCIA DEL RIO 4041",
         "ip_address": "190.210.214.252"
      },
      "purchase_totals": {
         "currency": "ARS",
         "amount": 2
      },
      "channel": "Web",
      "customer_in_site": {
         "days_in_site": 243,
         "is_guest": False,
         "password": "abracadabra",
         "num_of_transactions": 1,
         "cellphone_number": "12121"
      },
      "device_unique_id": "devicefingerprintid",
      "travel_transaction_data": {
          "reservation_code": "GJH784",
        "third_party_booking": False,
        "departure_city": "EZE",
        "final_destination_city": "HND",
        "international_flight": True,
        "frequent_flier_number": "00000123",
        "class_of_service": "class" ,
        "day_of_week_of_flight": 2,
        "week_of_year_of_flight": 5,
        "airline_code": "AA",
        "code_share": "SKYTEAM",
        "decision_manager_travel": {
            "complete_route": "EZE-LAX:LAX-HND",
            "journey_type": "one way",
            "departure_date": {
                "departure_time": "2017-05-30T09:00Z",
                "departure_zone": "GMT-0300"
            }
        },
        "passengers": [{
            "email": "juan@mail.com",
            "first_name": "Juan",
            "last_name": "Perez",
            "passport_id": "412314851231",
            "phone": "541134356768",
            "passenger_status": "gold",
            "passenger_type": "ADT"
            }
         ],
         "airline_number_of_passengers": 1
      }
   }

 }

validationData_Swatch_CS_RetailTP  = {
     "site": {
         "transaction_id": "Swatch CS RetailTP {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/es_ar/",
     "cancel_url": "https://shop.swatch.com/es_ar/",
"fraud_detection": {
      "send_to_cs": True,
      "channel": "Web/Mobile/Telefonica",
      "bill_to": {
        "city": "Buenos Aires",
         "country": "AR",
         "customer_id": "martinid",
         "email": "accept@decidir.com.ar",
         "first_name": "martin",
         "last_name": "paoletta",
         "phone_number": "1547766329",
         "postal_code": "1427",
         "state": "BA",
         "street1": "GARCIA DEL RIO 4041",
         "street2": "GARCIA DEL RIO 4041"
      },
      "purchase_totals": {
         "currency": "ARS",
         "amount": 2
      },
      "customer_in_site": {
         "days_in_site": 243,
         "is_guest": False,
         "password": "abracadabra",
         "num_of_transactions": 1,
         "cellphone_number": "12121",
         "date_of_birth": "129412",
         "street": "RIO 4041"
      },
      "retail_transaction_data": {
         "ship_to": {
            "city": "Buenos Aires",
            "country": "AR",
            "email": "accept@decidir.com.ar",
            "first_name": "martin",
            "last_name": "paoletta",
            "phone_number": "1547766329",
            "postal_code": "1427",
            "state": "BA",
            "street1": "GARCIA DEL RIO 4041",
            "street2": "GARCIA DEL RIO 4041"
      },
         "days_to_delivery": "55",
         "dispatch_method": "storepickup",
         "tax_voucher_required": True,
         "customer_loyality_number": "123232",
         "coupon_code": "cupon22",
         "items": [
            {
               "code": "popblacksabbat2016",
               "description": "Popular Black Sabbath 2016",
               "name": "popblacksabbat2016ss",
               "sku": "asas",
               "total_amount": 20,
               "quantity": 1,
               "unit_price": 20
            },
           {
              "code": "popblacksdssabbat2016",
              "description": "Popular Blasdsck Sabbath 2016",
              "name": "popblacksabbatdsds2016ss",
              "sku": "aswewas",
              "total_amount": 111212,
              "quantity": 1,
              "unit_price": 111212
           }
         ]
      },
        "csmdds": [
         {"code": 17, "description": "Campo MDD17"},
          {"code": 18, "description": "Campo MDD18"},
         {"code": 19, "description": "Campo MDD19"},
         {"code": 20, "description": "Campo MDD20"},
         {"code": 21, "description": "Campo MDD21"},
         {"code": 22, "description": "Campo MDD22"},
         {"code": 23, "description": "Campo MDD23"},
         {"code": 24, "description": "Campo MDD24"},
         {"code": 25, "description": "Campo MDD25"},
         {"code": 26, "description": "Campo MDD26"},
         {"code": 27, "description": "Campo MDD27"},
         {"code": 28, "description": "Campo MDD28"},
         {"code": 29, "description": "Campo MDD29"},
         {"code": 30, "description": "Campo MDD30"},
         {"code": 31, "description": "Campo MDD31"},
         {"code": 32, "description": "Campo MDD32"},
         {"code": 33, "description": "Campo MDD33"},
         {"code": 34, "description": "Campo MDD34"},
         {"code": 43, "description": "Campo MDD43"},
         {"code": 44, "description": "Campo MDD44"},
         {"code": 45, "description": "Campo MDD45"},
         {"code": 46, "description": "Campo MDD46"},
         {"code": 47, "description": "Campo MDD47"},
         {"code": 48, "description": "Campo MDD48"},
         {"code": 49, "description": "Campo MDD49"},
         {"code": 50, "description": "Campo MDD50"},
         {"code": 51, "description": "Campo MDD51"},
         {"code": 52, "description": "Campo MDD52"},
         {"code": 53, "description": "Campo MDD53"},
         {"code": 54, "description": "Campo MDD54"},
         {"code": 55, "description": "Campo MDD55"},
         {"code": 56, "description": "Campo MDD56"},
         {"code": 57, "description": "Campo MDD57"},
         {"code": 58, "description": "Campo MDD58"},
         {"code": 59, "description": "Campo MDD59"},
         {"code": 60, "description": "Campo MDD60"},
         {"code": 61, "description": "Campo MDD61"},
         {"code": 62, "description": "Campo MDD62"},
         {"code": 63, "description": "Campo MDD63"},
         {"code": 64, "description": "Campo MDD64"},
         {"code": 65, "description": "Campo MDD65"},
         {"code": 66, "description": "Campo MDD66"},
         {"code": 67, "description": "Campo MDD67"},
         {"code": 68, "description": "Campo MDD68"},
         {"code": 69, "description": "Campo MDD69"},
         {"code": 70, "description": "Campo MDD70"},
         {"code": 71, "description": "Campo MDD71"},
         {"code": 72, "description": "Campo MDD72"},
         {"code": 73, "description": "Campo MDD73"},
         {"code": 74, "description": "Campo MDD74"},
         {"code": 75, "description": "Campo MDD75"},
         {"code": 76, "description": "Campo MDD76"},
         {"code": 77, "description": "Campo MDD77"},
         {"code": 78, "description": "Campo MDD78"},
         {"code": 79, "description": "Campo MDD79"},
         {"code": 80, "description": "Campo MDD80"},
         {"code": 81, "description": "Campo MDD81"},
         {"code": 82, "description": "Campo MDD82"},
         {"code": 83, "description": "Campo MDD83"},
         {"code": 84, "description": "Campo MDD84"},
         {"code": 85, "description": "Campo MDD85"},
         {"code": 86, "description": "Campo MDD86"},
         {"code": 87, "description": "Campo MDD87"},
         {"code": 88, "description": "Campo MDD88"},
         {"code": 89, "description": "Campo MDD89"},
         {"code": 90, "description": "Campo MDD90"},
         {"code": 91, "description": "Campo MDD91"},
         {"code": 92, "description": "Campo MDD92"},
         {"code": 93, "description": "Campo MDD93"},
         {"code": 94, "description": "Campo MDD94"},
         {"code": 95, "description": "Campo MDD95"},
         {"code": 96, "description": "Campo MDD96"},
         {"code": 97, "description": "Campo MDD97"},
         {"code": 98, "description": "Campo MDD98"},
         {"code": 99, "description": "Campo MDD99"}
      ]
   }

 }



txSimpleVisa_Swatch = {
    "cardNumber": "4509790113276723",
    "cardExpiration": "1220",
    "securityCode": "123",
    "cardHolderName": "a swiss man",
    "siteId": "28464383",
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


validationData_Swatch = {
     "site": {
         "transaction_id": "Swatch {}".format(str(int(time.time()))),
         "template": {
             "id": 4
         }
     },
     "customer": {
         "id": "001",
         "email" : "juan.rego@redb.ee"
     },
     "payment": {
         "amount": 30000,
         "currency": "ARS",
         "payment_method_id":1,
         #"bin": "450979",
         "installments" : 4,
         "payment_type": "single",
         "sub_payments" : []
     },
     "success_url": "https://www.swatch.com/",
    "cancel_url": "https://www.swatch.com/es_ar/"
}

validationData_Swatch_RedirectURL = validationData_Swatch.copy()
validationData_Swatch_RedirectURL.pop("success_url")
validationData_Swatch_RedirectURL["redirect_url"] = "https://www.swatch.com/es_ar/"