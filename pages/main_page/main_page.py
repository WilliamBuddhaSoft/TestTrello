from base.basepage import BasePage
from pages.board_page.board_page import BoardPage
import utilities.custom_logger as cl
import base.base_requests as req
import time
import logging


class MainPage(BasePage):

    log = cl.custom_logger(logging.DEBUG)
    req = req.BaseRequests()

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _create_personal_board = ".//div[@class='js-react-root']/div/div[1]//span[contains(text(), 'Create new board…')]"
    _myBoard_bar = ".//*[@id='content']//*[@href='/b/hGlywI4f/public-board']"
    _public_board_board_sharing = "public"
    _team_board_board_sharing = "team"
    _private_board_board_sharing = "private"
    _change_privacy_button = ".//a[contains(text(), 'Change')]"

    def openBoard(self, board_name):
        self.element_click(".//span[contains(text(), '" + str(board_name) + "')]/../parent::a[@class='board-tile']", 'xpath')

    def createBoard(self):
        self.element_click(self._create_personal_board, 'xpath')
        new_board_name = "BOARD_TEST"+str(round(time.time() * 1000))
        self.send_keys(new_board_name, ".//*[@id='boardNewTitle']", 'xpath')
        self.element_click(self._change_privacy_button, 'xpath')
        self.element_click(self._public_board_board_sharing, 'name')
        self.element_click(".//input[@type='submit' and starts-with(@class, 'primary')]", 'xpath')
        return new_board_name

    def deleteBoard(self, board_name):
        self.wait_for_element(".//a[contains(text(), 'More')]", 'xpath', 3)
        self.element_click(".//a[contains(text(), 'More')]", 'xpath')
        self.element_click(".//a[contains(text(), 'Close Board')]", 'xpath')
        self.element_click(".//input[@type='submit' and starts-with(@class, 'js-confirm')]", 'xpath')
        self.element_click(".//a[contains(text(), 'Permanently Delete Board')]", 'xpath')
        self.element_click(".//input[@type='submit']", 'xpath')

    def verifyBoardCreated(self, board_name):
        bp = BoardPage(self.driver)
        bp.wait_for_element('board')
        result = self.element_presence_check(".//span[contains(text(),'" + str(board_name) + "')]/parent::a[starts-with(@class,'board-header-btn')]", 'xpath')

        return result

    def verifyBoardDeletion(self):
        self.wait_for_element(".//*[contains(text(), 'Board not found.')]", 'xpath', )
        result = self.element_presence_check(".//*[contains(text(), 'Board not found.')]", 'xpath')

        return result





