from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

class ExtendedWebElement (WebElement):

    def fill (self,data):
        if self.tag_name == "input":
            try:
                self.clear()
            except Exception:
                pass
            self.send_keys(data)
        elif self.tag_name == "select":
            Select(self).select_by_value(data)
