from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
import unittest
import pytest

@pytest.mark.usefixtures("setUp")
class LoginTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def classSetup(self, setUp):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)

    def test_validLogin(self):
        self.lp.login("lidochka@mfsa.ru", "123qwe123")
        result = self.lp.verifyLoginSuccessful()
        self.ts.mark_final("test_validLogin", result, "Login Verification")

    def test_invalidLogin(self):
        self.lp.login("kakashka", "kakashka")
        result = self.lp.verifyLoginFailed()
        self.ts.mark_final("test_invalidLogin", result, "Login Verification")