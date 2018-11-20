import os
from settings import *
from test_WebTx import BaseTest

class BaseTestForms(BaseTest):

    def setUp(self):
        super(BaseTestForms, self).setUp()
        self.formsBaseURL = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["baseURL"]
        self.formsPort = environments[os.getenv("ENVIRONMENT", defaultEnvironment)]["forms"]["port"]