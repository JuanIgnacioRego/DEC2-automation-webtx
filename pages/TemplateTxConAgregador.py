from pages.BasePage import BasePage

class TemplateTxConAgregador(BasePage):

    def __init__(self, driver, baseURL, port):
        self.link = "/forms/test/TestCompraA.html"
        BasePage.__init__(self, driver, baseURL, port, self.link)
