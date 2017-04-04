from pages.main_page.main_page import MainPage
from pages.home.login_page import LoginPage
from utilities.teststatus import TestStatus
from utilities.custom_logger import custom_logger
import unittest
import pytest

@pytest.mark.usefixtures("setUp")
class CreateBoardTest(unittest.TestCase):

    cl = custom_logger()

    @pytest.fixture(autouse=True)
    def classSetup(self, setUp):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.lp.login('lidochka@mfsa.ru', '123qwe123')
        self.mp = MainPage(self.driver)

    def test_deleteBoard(self):
        self.lp.verifyLoginSuccessful()
        new_board = self.mp.createBoard()
        self.mp.deleteBoard(new_board)
        result = self.mp.verifyBoardDeletion()
        self.ts.mark_final('test_deleteBoard', result, 'Board Deletion')


    def test_createBoard(self):
        self.lp.verifyLoginSuccessful()
        new_board = self.mp.createBoard()
        result = self.mp.verifyBoardCreated(new_board)
        self.ts.mark_final('test_CreateBoard', result, 'Board Creation')
        self.mp.deleteBoard(new_board)
