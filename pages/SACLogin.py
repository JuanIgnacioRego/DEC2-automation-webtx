# -*- coding: utf-8 -*-
from pages.BasePage import BasePage
from settings import environments, defaultEnvironment
import os
class SACLogin(BasePage):

    def __init__(self, driver):
        self.baseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["baseURL"]
        self.port = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["port"]
        self.link = "/sac/LoginServlet"
        BasePage.__init__(self, driver, self.baseURL, self.port, self.link)

    def login(self):
        self.usuariosps.fill (environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["user"])
        self.passwordsps.fill (environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["password"])
        self.passwordsps.submit()
        self.assertSucessfulLogin()

    def assertSucessfulLogin(self):
        if self.driver.current_url.endswith("/sac/LoginServlet"):
            alert = self.driver.find_elements_by_xpath("//div[@class='txtrojochico']")
            if len(alert):
                if "No se han podido verificar los datos ingresados" in alert[0].text:
                    raise Exception ("Username/password ({}/{}) wrong.".format( \
                        environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["user"], \
                        environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["SACLogin"]["password"]))
