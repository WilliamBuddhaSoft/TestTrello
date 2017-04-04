from pages.home.login_page import LoginPage
from pages.main_page.main_page import MainPage
from pages.board_page.board_page import BoardPage
from utilities.teststatus import TestStatus
from utilities.custom_logger import custom_logger
from base.base_requests import BaseRequests
import unittest
import pytest
import time


@pytest.mark.usefixtures("setUp")
class CardTest(unittest.TestCase):

    cl = custom_logger()
    br = BaseRequests()

    @pytest.fixture(autouse=True)
    def classSetup(self, setUp):
        # Login with "lidochka1" credentials
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.lp.login("lidochka@mfsa.ru", "123qwe123")

    @pytest.mark.run(order=0)
    def test_crateCard(self):
        self.mp = MainPage(self.driver)
        # Create new board
        board = self.mp.createBoard()
        # Get new board id
        board_id = self.br.get_board_id('lidochka1', board)

        self.bp = BoardPage(self.driver)
        new_list = self.bp.createList()
        list_id = self.br.get_list_id(board_id, new_list)

        self.bp.element_click(".//a[contains(text(), 'Add a card')]", 'xpath')
        new_card = self.bp.createCard()
        result = self.bp.verifyCardCreated(list_id, new_card)

        self.ts.mark_final('test_createCard', result, 'Add new card test')
        self.mp.deleteBoard(board)

    @pytest.mark.run(order=2)
    def test_cardDragNDrop(self):
        self.mp = MainPage(self.driver)
        board = self.mp.createBoard()
        board_id = self.br.get_board_id('lidochka1', board)

        self.bp = BoardPage(self.driver)
        first_list = self.bp.createList()
        first_list_id = self.br.get_list_id(board_id, first_list)

        self.bp.element_click(".//a[contains(text(), 'Add a card')]", 'xpath')
        new_card = self.bp.createCard()
        new_card_id = self.br.get_card_id(first_list_id, new_card)

        self.bp.element_click(".//span[contains(text(), 'Add a list')]", 'xpath')
        second_list = self.bp.createList()
        second_list_id = self.br.get_list_id(board_id, second_list)

        new_card_locator = "//a[starts-with(@class,'list-card-title') and contains(text(), '"+str(new_card)+"')]/parent::div"
        self.bp.dragAndDrop(new_card_locator)
        time.sleep(3)
        result = self.bp.verifyCardInList(new_card_id, second_list_id)
        self.ts.mark_final('test_cardDragNDrop', result, 'Verify if card dragged and dropped')

        self.bp.deleteBoard(board)

    @pytest.mark.run(order=1)
    def test_deleteCard(self):
        self.mp = MainPage(self.driver)
        board = self.mp.createBoard()
        board_id = self.br.get_board_id('lidochka1', board)

        self.bp = BoardPage(self.driver)
        self.bp.createList()

        self.bp.element_click(".//a[contains(text(), 'Add a card')]", 'xpath')
        new_card = self.bp.createCard()
        new_card_locator = "//a[starts-with(@class,'list-card-title') and contains(text(), '"+str(new_card)+"')]/parent::div"

        self.bp.deleteCard(new_card_locator)
        time.sleep(3)
        result = self.bp.verifyCardDeleted(board_id, new_card)
        self.ts.mark_final('test_deleteCard', result, 'Delete card')

        self.bp.deleteBoard(board)

    def test_createList(self):
        self.mp = MainPage(self.driver)
        board = self.mp.createBoard()
        board_id = self.br.get_board_id('lidochka1', board)
        self.bp = BoardPage(self.driver)
        new_list = self.bp.createList()
        result = self.bp.verifyListCreated(board_id, new_list)
        self.ts.mark_final('test_createList', result, 'Create new list')
        time.sleep(3)
        self.bp.deleteBoard(board)

    def test_deleteList(self):
        self.mp = MainPage(self.driver)
        board = self.mp.createBoard()
        board_id = self.br.get_board_id('lidochka1', board)
        self.bp = BoardPage(self.driver)
        new_list = self.bp.createList()
        self.bp.deleteList(new_list)
        result = self.bp.verifyListDeleted(new_list, board_id)
        self.ts.mark_final('test_deleteList', result, 'Create new list')
        self.bp.deleteBoard(board)




