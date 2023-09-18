# Configuration for Trello API interaction
import os

BASE_URL = 'https://api.trello.com/1/'

API_KEY = os.environ.get('TRELLO_API_KEY')
API_TOKEN = os.environ.get('TRELLO_API_TOKEN')

BOARD_ID = os.environ.get('TRELLO_BOARD_ID')

TO_DO_LIST_NAME = 'To Do'
DONE_LIST_NAME = 'Done'
