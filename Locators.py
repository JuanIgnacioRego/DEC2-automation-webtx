from selenium.webdriver.common.by import By

class TemplateCompraSimpleLocators:
    NROCOMERCIO = (By.NAME, "NROCOMERCIO")
    NROOPERACION = (By.NAME, "NROOPERACION")
    MONTO = (By.NAME, "MONTO")
    CUOTAS = (By.NAME, "CUOTAS")
    URLDINAMICA = (By.NAME, "URLDINAMICA")
    MONEDA = (By.NAME, "MONEDA")
    MEDIODEPAGO = (By.NAME, "MEDIODEPAGO")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    IDTEMPLATES = (By.NAME, "IDTEMPLATES")
    FECHAVTO = (By.NAME, "FECHAVTO")
    PARAMSITIO = (By.NAME, "PARAMSITIO")
    JSESSIONID = (By.NAME, "JSESSIONID")
    URLREDIRECT = (By.NAME, "URLREDIRECT")
    CLAVE = (By.ID, "CLAVE")
    IDTRANSACCION = (By.ID, "IDTRANSACCION")
    IDPLAN = (By.NAME, "IDPLAN")
    SUBMIT = (By.NAME, "SUBMIT")
    
class TemplateCompraDistribuidaLocators:
    NROCOMERCIO = (By.NAME, "NROCOMERCIO")
    NROOPERACION = (By.NAME, "NROOPERACION")
    MONTO = (By.NAME, "MONTO")
    CUOTAS = (By.NAME, "CUOTAS")
    URLDINAMICA = (By.NAME, "URLDINAMICA")
    MONEDA = (By.NAME, "MONEDA")
    MEDIODEPAGO = (By.NAME, "MEDIODEPAGO")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    FECHAVTO = (By.NAME, "FECHAVTO")
    FECHAVTOCUOTA1 = (By.NAME, "FECHAVTOCUOTA1")
    IDMODALIDAD = (By.NAME, "IDMODALIDAD")
    SITEDIST = (By.NAME, "SITEDIST")
    CUOTASDIST = (By.NAME, "CUOTASDIST")
    IMPDIST = (By.NAME, "IMPDIST")
    BIN = (By.NAME, "BIN")
    TIPODOC = (By.NAME, "TIPODOC")
    NRODOC = (By.NAME, "NRODOC")
    IDTEMPLATES = (By.NAME, "IDTEMPLATES")
    PARAMSITIO = (By.NAME, "PARAMSITIO")
    EXTRA = (By.NAME, "EXTRA")
    SEXOTITULAR = (By.NAME, "SEXOTITULAR")
    CLAVE = (By.NAME, "CLAVE")
    IDTRANSACCION = (By.NAME, "IDTRANSACCION")
    IDPLAN = (By.NAME, "IDPLAN")
    #LEYENDADEPAGO = (By.NAME, "LEYENDADEPAGO")
    #DATOSADICIONALES = (By.NAME, "DATOSADICIONALES")
    SUBMIT = (By.NAME, "SUBMIT")

class TemplateTxConAgregadorLocators(object):
    aindicador = (By.NAME, "aindicador")
    adocumento = (By.NAME, "adocumento")
    afactpagar = (By.NAME, "afactpagar")
    afactdevol = (By.NAME, "afactdevol")
    anombrecom = (By.NAME, "anombrecom")
    adomiciliocomercio = (By.NAME, "adomiciliocomercio")
    anropuerta = (By.NAME, "anropuerta")
    acodpostal = (By.NAME, "acodpostal")
    arubro = (By.NAME, "arubro")
    acodcanal = (By.NAME, "acodcanal")
    acodgeografico = (By.NAME, "acodgeografico")
    NROCOMERCIO = (By.NAME, "NROCOMERCIO")
    NROOPERACION = (By.NAME, "NROOPERACION")
    MONTO = (By.NAME, "MONTO")
    CUOTAS = (By.NAME, "CUOTAS")
    URLDINAMICA = (By.NAME, "URLDINAMICA")
    MONEDA = (By.NAME, "MONEDA")
    MEDIODEPAGO = (By.NAME, "MEDIODEPAGO")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    IDTEMPLATES = (By.NAME, "IDTEMPLATES")
    FECHAVTO = (By.NAME, "FECHAVTO")
    PARAMSITIO = (By.NAME, "PARAMSITIO")
    JSESSIONID = (By.NAME, "JSESSIONID")
    URLREDIRECT = (By.NAME, "URLREDIRECT")
    SUBMIT = (By.NAME, "SUBMIT")

class ValidationVisaLocators(object):
    NOMBREENTARJETA = (By.NAME,"NOMBREENTARJETA")
    NROTARJETA = (By.NAME,"NROTARJETA")
    idComboMes = (By.ID,"idComboMes")
    idComboAno = (By.ID,"idComboAno")
    CODSEGURIDAD = (By.NAME,"CODSEGURIDAD")
    EMAILCLIENTE = (By.NAME,"EMAILCLIENTE")
    TIPODOC = (By.NAME,"TIPODOC")
    NRODOC = (By.NAME,"NRODOC")
    CALLE = (By.NAME,"CALLE")
    NROPUERTA = (By.NAME,"NROPUERTA")
    FECHANACIMIENTO = (By.NAME,"FECHANACIMIENTO")
    SUBMIT = (By.NAME, "ok")

class ValidationMastercardLocators:
    NOMBREENTARJETA = (By.NAME, "NOMBREENTARJETA")
    NROTARJETA = (By.NAME, "NROTARJETA")
    VENCTARJETA = (By.NAME, "VENCTARJETA")
    CODSEGURIDAD = (By.NAME, "CODSEGURIDAD")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    SUBMIT = (By.NAME, "ok")

class ValidationNativaLocators:
    NOMBREENTARJETA = (By.NAME, "NOMBREENTARJETA")
    NROTARJETA = (By.NAME, "NROTARJETA")
    VENCTARJETA = (By.NAME, "VENCTARJETA")
    CODSEGURIDAD = (By.NAME, "CODSEGURIDAD")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    TIPODOC = (By.NAME,"TIPODOC")
    NRODOC = (By.NAME,"NRODOC")
    CALLE = (By.NAME,"CALLE")
    NROPUERTA = (By.NAME,"NROPUERTA")
    FECHANACIMIENTO = (By.NAME,"FECHANACIMIENTO")
    SUBMIT = (By.NAME, "ok")

class ValidationAmexLocators(object):
    NOMBREENTARJETA = (By.NAME, "NOMBREENTARJETA")
    NROTARJETA = (By.NAME, "NROTARJETA")
    VENCTARJETA = (By.NAME, "VENCTARJETA")
    CODSEGURIDAD = (By.NAME, "CODSEGURIDAD")
    EMAILCLIENTE = (By.NAME, "EMAILCLIENTE")
    TIPODOC = (By.NAME, "TIPODOC")
    #NRODOC = (By.NAME, "NRODOC")
    SEXOTITULAR = (By.NAME, "SEXOTITULAR")
    SUBMIT = (By.NAME, "ok")

class ConfirmTxLocators:
    CONFIRMAR = (By.NAME, "submit")

class SACLoginLocators(object):
    usuariosps = (By.NAME, "usuariosps")
    passwordsps = (By.NAME, "passwordsps")

class SACInicioLocators(object):
    consulta = (By.NAME, "b_consultaform")

class SACTxHistoryLocators(object):
    pass

class TemplateIturanLocators:
    NOMBREENTARJETA = (By.NAME, "card_data.card_holder_name")
    NROTARJETA = (By.NAME, "card_data.card_number")
    idComboMes = (By.NAME, "card_data.card_expiration_month")
    idComboAno = (By.NAME, "card_data.card_expiration_year")
    CODSEGURIDAD = (By.NAME, "card_data.security_code")
    NRODOC = (By.NAME, "card_data.card_holder_identification.number")
    SUBMIT = (By.ID, "send-button")

class TemplateIturanResultLocators:
    resultMessage = (By.CLASS_NAME, "amount-label")

class TemplateSwatchLocators:
    cardHolderName = (By.ID, "cardHolderName")
    cardNumber = (By.ID, "cardNumber")
    cardExpiration = (By.ID, "cardExpiration")
    securityCode = (By.ID, "securityCode")
    securityCodeHelp = (By.ID, "cvvHelpButton")
    submit = (By.XPATH, "//button[@type='submit']")
    #cancel = (By.ID, "cancel-button")
    #amount = (By.CLASS_NAME, "amount-box-installments")
    #installments = (By.CLASS_NAME, "amount-box-total")
    #headerImage = (By.ID, "headerImage")
    #footerImage = (By.ID, "footerImage")

class TemplateSwatchResultLocaltors:
    pass

class TemplateAFIPFormLocators:
    NOMBREENTARJETA = (By.ID, "Nombre")
    NROTARJETA = (By.ID, "NumeroTarjeta")
    idComboMes = (By.NAME, "card_data.card_expiration_month")
    idComboAno = (By.NAME, "card_data.card_expiration_year")
    #CODSEGURIDAD = (By.XPATH, "//input[@id='cvc']")
    SUBMIT = (By.ID, "boton-pagar")

class RequestBinLocators:
    pass