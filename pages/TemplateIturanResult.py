from pages.BasePage import BasePage

class TemplateIturanResult(BasePage):

    def __init__(self, driver):
        BasePage.__init__(self,driver)

    def getTxStatus(self):
        return (self.resultMessage.text == "Su pago ha sido exitoso!")

    def getTxResultDetails(self):
        if self.getTxStatus():
            txId = self.driver.find_elements_by_css_selector(".card-block.amount-value.read-only")[0].text
            amount = self.driver.find_elements_by_css_selector(".card-block.amount-value.read-only")[1].text
            date =  self.driver.find_elements_by_css_selector(".card-block.amount-value.read-only")[2].text

            return (txId, amount, date)
        else:

            errorType = self.driver.find_elements_by_css_selector(".card-block.amount-value.read-only")[0].text

            return (errorType)