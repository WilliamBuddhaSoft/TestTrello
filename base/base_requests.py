import requests
from utilities.custom_logger import custom_logger
import time
import os


API_KEY = os.environ.get("API_KEY")
API_TOKEN = os.environ.get("API_TOKEN")


class TrelloClient:
    URL_BASE = "https://api.trello.com/1/%s"
    URL_MEMBERS = URL_BASE % "members/{username}"
    URL_BOARDS = URL_BASE % "boards/{board_id}"
    URL_LISTS = URL_BASE % "lists/{list_id}"
    URL_CARDS = URL_BASE % "cards/{card_id}"

    @classmethod
    def get_members(cls, username):
        json = requests.get(cls.URL_MEMBERS.format(username=username), {'fields': 'id'}).json()
        return json

    @classmethod
    def get_boards(cls, username):
        json = requests.get("%s/boards" % cls.URL_MEMBERS.format(username=username), {'fields': 'name', 'key': API_KEY}).json()
        return json

    @classmethod
    def get_lists(cls, board_id):
        json = requests.get("%s/lists" % cls.URL_BASE.format(board_id=board_id), {'fields': 'name', 'key': API_KEY}).json()
        return json

    @classmethod
    def get_member_cards(cls, username):
        json = requests.get("%s/cards" % cls.URL_MEMBERS.format(username=username), {'fields': 'name,idBoard,idList', 'key': API_KEY}).json()
        return json

    @classmethod
    def get_board_cards(cls, board_id):
        json = requests.get("%s/cards" % cls.URL_BOARDS.format(board_id=board_id), {'fields': 'name,idList', 'key': API_KEY}).json()
        return json

    @classmethod
    def get_list_cards(cls, list_id):
        json = requests.get("%s/cards" % cls.URL_LISTS.format(list_id=list_id), {'fields': 'name', 'key': API_KEY}).json()
        return json


class BaseRequests:

    cl = custom_logger()

    def get_member_id(self, username):
        json = TrelloClient.get_members(username)
        return json.get('id')

    def get_boards(self, username):
        boards = TrelloClient.get_boards(username)

        if boards != {}:
            self.cl.info('Boards IDs and names was taken for user %s' % username)
        else:
            self.cl.warn('No boards found for user %s' % username)

        return boards

    def get_board_id(self, username, board_name):
        board_id = ''
        time.sleep(3)
        json = TrelloClient.get_boards(username)
        for i in json:
            if i.get('name') == board_name:
                board_id = i.get('id')
                self.cl.info('%s board ID was taken' % board_name)

        if board_id == '':
            self.cl.warn('Board %s not found' % board_name)

        return board_id

    def get_lists(self, board_id):
        lists = TrelloClient.get_lists(board_id)
        if lists is not None:
            self.cl.info('Lists IDs and names was taken for board %s' % board_id)
        else:
            self.cl.warn('No lists fount on board %s' % board_id)

        return lists

    def get_list_id(self, board_id, list_name):
        list_id = ''
        json = TrelloClient.get_lists(board_id)

        for i in json:
            if i.get('name') == list_name:
                list_id = i.get('id')
                self.cl.info('%s list ID was taken' % list_name)

        if list_id == '':
            self.cl.warn('List %s not found' % list_name)

        return list_id

    def get_board_cards(self, board_id):
        cards = TrelloClient.get_board_cards(board_id)

        if cards is None:
            self.cl.warn('Cards not found on board %s' % board_id)
        else:
            self.cl.info('For board %s cards info was collected' % board_id)

        return cards

    def get_list_cards(self, list_id):
        cards = TrelloClient.get_list_cards(list_id)

        if cards is None:
            self.cl.warn('Cards not found on list %s' % list_id)
        else:
            self.cl.info('For list %s cards info was collected' % list_id)

        return cards

    def get_card_id(self, list_id, card_name):
        card_id = ''
        cards = TrelloClient.get_list_cards(list_id)

        for i in cards:
            if i.get('name') == card_name:
                card_id = i.get('id')
                self.cl.info('%s card ID, from list, was taken' % card_name)

        if card_id == '':
            self.cl.warn('Card %s not found' % card_name)

        return card_id

    def get_member_cards(self, username):
        cards = TrelloClient.get_member_cards(username)

        if cards == {}:
            self.cl.warn('Cards not found for user %s' % username)
        else:
            self.cl.info('%s cards info was collected' % username)
            return cards

        return None
