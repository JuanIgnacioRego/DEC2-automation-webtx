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
