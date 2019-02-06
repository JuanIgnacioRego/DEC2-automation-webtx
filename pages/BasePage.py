from tools.ExtendedWebElement import ExtendedWebElement
from selenium.common.exceptions import NoSuchElementException
from Exceptions import URLStatusCodeNot200Exception

import requests

class BasePage(object):

    def __init__(self, driver, baseURL="", port="", link=""):
        self.driver = driver
        self.baseURL = baseURL
        self.port = port
        self.link = link
        if self.link: self.driver.get("http://"+self.baseURL+ ":" + self.port + self.link)
        exec (("from Locators import %s as l") % (self.__class__.__name__ + "Locators"))
        for attr in [attr for attr in l.__dict__.keys() if not attr.startswith("__")]:
            try:
                WE = self.driver.find_element(*getattr(l, attr))
                setattr(self, attr, ExtendedWebElement(WE.parent, WE.id))
            except NoSuchElementException as error:
                response = requests.get(self.driver.current_url)
                if response.ok:
                    print (error)
                else:
                    raise URLStatusCodeNot200Exception("URL {} is not reachable. \n"
                                                       "Requesting a /GET to this direction "
                                                       "returns a status code different from 200 [OK]. \n"
                                                       "Status code received: {}.\n Message: {}".format
                                                       (self.driver.current_url, response.status_code, response.text))


