from tools.ExtendedWebElement import ExtendedWebElement

class BasePage(object):

    def __init__(self, driver, baseURL="", port="", link=""):
        self.driver = driver
        self.baseURL = baseURL
        self.port = port
        self.link = link
        if self.link: self.driver.get("http://"+self.baseURL+ ":" + self.port + self.link)
        exec (("from Locators import %s as l") % (self.__class__.__name__ + "Locators"))
        for attr in [attr for attr in l.__dict__.keys() if not attr.startswith("__")]:
            WE = self.driver.find_element(*getattr(l, attr))
            setattr(self, attr, ExtendedWebElement(WE.parent, WE.id))
