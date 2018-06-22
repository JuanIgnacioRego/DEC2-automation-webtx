from pages.BasePage import BasePage

class TemplateCompraDistribuida(BasePage):

    def __init__(self, driver, baseURL, port):
        self.link = "/forms/test/TestCompra-Dist.html"
        BasePage.__init__(self, driver, baseURL, port, self.link)
