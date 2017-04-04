import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from pages.main_page.main_page import MainPage

class LoginPage(BasePage):

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _login_button = "html/body/div[1]/div[2]/a[1]"
    _email_field = "user"
    _password_field = "password"
    _submit_button = "login"


    def enterEmail(self, email):
        self.send_keys(email, self._email_field)

    def enterPassword(self, password):
        self.send_keys(password, self._password_field)

    def clickLoginButton(self):
        self.element_click(self._submit_button)

    def login(self, email="", password=""):
        self.element_click(self._login_button, 'xpath')
        self.enterEmail(email)
        self.enterPassword(password)
        self.element_click(self._submit_button)
        self.element_click(self._submit_button)

    def verifyLoginSuccessful(self):
        main_page = MainPage(self.driver)
        # main_page.wait_for_element(".//h3[contains(text(), 'Personal Boards')]")
        result = self.element_presence_check(".//h3[contains(text(), 'Personal Boards')]", 'xpath')
        return result

    def verifyLoginFailed(self):
        result = self.is_element_present(".//*[@id='error']",
                                         locator_type="xpath")
        return result