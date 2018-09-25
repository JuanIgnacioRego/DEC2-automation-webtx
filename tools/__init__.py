TraduccionCamposWebTx_SAC = {
    "ID op." : "NROOPERACION",
    "Site" : "NROCOMERCIO",
    "Monto" : "MONTO",
    "Cuotas" : "CUOTAS",
    "Titular" : "NOMBREENTARJETA",
    "e-mail" : "EMAILCLIENTE",
    "Nro Doc": "NRODOC"
}

translationRequestBin_SAC = {
    "monto":"MONTO",
    "nrodoc":"NRODOC",
    "titular":"NOMBREENTARJETA",
    "noperacion":"NROOPERACION",
    "emailcomprador": "EMAILCLIENTE",
    "resultado":"RESULTADO",
    "nrotarjetavisible":"NROTARJETAVISIBLE",
    "fechahora":"FECHAHORA",
    "cuotas":"CUOTAS"
}

def convertDictToWebTx(dict, translationDict):
    """
    :param dict: dict with structure fieldName:value, for example='titular': "I'm VISA"
    :param translationDict: dict with structure fieldName: fieldNameinWebTx, for example="titular":"NOMBREENTARJETA",
    :return: dict with WebTx fields as keys. Keys that don't appear in translationDict will be erased.
    """
    webTxDict = {}
    for key in dict.keys():
        if key in translationDict.keys():
            webTxDict[translationDict[key]] = dict[key]
    return webTxDict

def processData(values):
    """
    This method converts the original provided data to run a tx into its final values. For example,
    amount field ("MONTO") is sent without float format and thier two last numbers
    will be converted to cents when the tx is run. So, an original amount = 20000
    will be formatted to 200,00.
    :param dict: a dict that contains tx values
    :return: same dict with values converted to the format that should have after tx is processed.
    """
    #This converts amount from the bare format (20000) to the real format (200,00)
    convertedValues = values.copy()
    if convertedValues.has_key("MONTO"): convertedValues["MONTO"] = convertedValues["MONTO"][:-2]+','+convertedValues["MONTO"][-2:]

    return convertedValues