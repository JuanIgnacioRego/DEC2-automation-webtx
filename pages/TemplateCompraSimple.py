from pages.BasePage import BasePage

class TemplateCompraSimple(BasePage):
    
    def __init__(self, driver, baseURL, port):
        self.link = "/forms/test/TestCompra.html"
        BasePage.__init__(self, driver, baseURL, port, self.link)
