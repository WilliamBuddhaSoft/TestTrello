import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from utilities.util import Util
from base.base_requests import BaseRequests
import time


class BoardPage(BasePage):

    log = cl.custom_logger(logging.DEBUG)
    br = BaseRequests()

    _new_card_text = ".list-card-composer-textarea.js-card-title"
    _first_list = ".//*[@id='board']/div[1]"
    _second_list = ".//*[@id='board']/div[2]"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def dragAndDrop(self, card_locator):
        ac = ActionChains(self.driver)
        ac.drag_and_drop(self.get_element(card_locator, 'xpath'), self.get_element(self._second_list, 'xpath')).perform()

    def createCard(self):
        util = Util()
        new_card = "test_"+str(util.get_unique_name())
        self.send_keys(new_card, self._new_card_text, 'css')
        time.sleep(3)
        self.element_click(".//*[@id='board']/div[1]//*[@type='submit']", 'xpath')
        return new_card

    def createList(self):
        util = Util()
        new_list = "test_"+str(util.get_unique_name())
        self.send_keys(new_list, ".//*[contains(@placeholder, 'Add a list')]", 'xpath')
        self.element_click(".//input[contains(@value, 'Save')]", 'xpath')
        return new_list

    def deleteCard(self, card_locator):
        self.element_click(card_locator, 'xpath')
        self.element_click(".//*[contains(@class,  'js-archive-card')]", 'xpath')
        self.element_click(".//*[contains(@class,  'js-delete-card')]", 'xpath')
        self.element_click("//*[@type='submit' and contains(@value, 'Delete')]", 'xpath')

    def deleteList(self, list_name):
        self.element_click(".//h2[contains(text()," + list_name + ")]/parent::div//child::div[@class='list-header-extras']", 'xpath')
        self.element_click(".//a[@class='js-close-list']", 'xpath')

    def deleteBoard(self, board_name):
        self.element_click(".//a[contains(text(), 'More')]", 'xpath')
        self.element_click(".//a[contains(text(), 'Close Board')]", 'xpath')
        self.element_click(".//input[@type='submit' and starts-with(@class, 'js-confirm')]", 'xpath')
        self.element_click(".//a[contains(text(), 'Permanently Delete Board')]", 'xpath')
        self.element_click(".//input[@type='submit']", 'xpath')

    def verifyCardCreated(self, list_id, card_name):
        result = self.element_presence_check(".//a[starts-with(@class, 'list-card-title') and contains(text(), '" + card_name + "')]", 'xpath')
        cards = self.br.get_list_cards(list_id)
        if result is True:
            for card in cards:
                if card.get('idList') == list_id and card.get('name') == card_name:
                    return True
        assert True == False
        return False

    def verifyListCreated(self,board_id, list_name):
        time.sleep(1)
        result = self.element_presence_check(".//h2[contains(text(), '" + list_name + "')]", 'xpath')
        print (result)
        lists = self.br.get_lists(board_id)
        print(lists)
        if result is True:
            for i in lists:
                if i.get('name') == list_name:
                    return True
        return False

    def verifyCardInList(self, card_id, list_id):
        cards = self.br.get_list_cards(list_id)
        for card in cards:
            if card.get('id') == card_id:
                return True
        return False

    def verifyCardDeleted(self, board_id, card_name):
        result = self.element_presence_check(".//a[starts-with(@class, 'list-card-title') and contains(text(), '" + card_name + "')]", 'xpath')
        json = self.br.get_board_cards(board_id)

        if result is False:
            for i in json:
                if i.get('name') == card_name:
                    return False
        else: return False

        return True

    def verifyListDeleted(self, list_name, board_id):
        time.sleep(1)
        result = self.element_presence_check(".//h2[contains(text(), '" + list_name + "')]", 'xpath')
        lists = self.br.get_lists(board_id)

        if result is False:
            if lists != []:
                for i in lists:
                    if i.get(list_name) is not None:
                        return False
            else: return True
        else:
            return False

        return True