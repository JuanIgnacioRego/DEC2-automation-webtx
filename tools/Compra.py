def Compra():


    cs = TemplateCompraSimple(self.driver, self.baseURL, self.port, "")
    for attr in [attr for attr in cs.__dict__.keys() if attr in compraSimpleData.keys()]:
        getattr(cs, attr).fill(compraSimpleData[attr])

    cs.SUBMIT.click()

    validacion = Validacion(self.driver)
    if validacion.wasApproved():
        for attr in [attr for attr in validacion.__dict__.keys() if attr in validacionData.keys()]:
            getattr(validacion, attr).fill(validacionData[attr])
        validacion.SUBMIT.click()

        # It verifies the Tx data that is displayed on screen when it was satisfactory.
        satisfactoryTxData = validacion.getSatisfactoryTxData()
        for key in list(set(compraSimpleData.keys() + validacionData.keys()).intersection(satisfactoryTxData.keys())):
            assert (
            compraSimpleData[key] if compraSimpleData.has_key(key) else validacionData[key] == satisfactoryTxData[key])

        # It verifies that satisfactory Tx was replicated on SAC.
        sacLogin = SACLogin(self.driver)
        sacLogin.login()
        sacInicio = SACInicio(self.driver)
        sacInicio.consulta.click()
        sacConsultaTransacciones = SACConsultaTransacciones(self.driver)

        sacTxData = sacConsultaTransacciones.getTx(satisfactoryTxData["NROOPERACION"])

        for key in sacTxData:
            assert (compraSimpleData[key] if compraSimpleData.has_key(key) else validacionData[key] == sacTxData[key])

    # It verifies that Tx was satisfactory or not, considering the expectedResult
    assert (validacion.wasApproved() == expectedResult)