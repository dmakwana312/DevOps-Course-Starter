# Configuration for Trello API interaction
import os

TO_DO_LIST_NAME = 'To Do'
DONE_LIST_NAME = 'Done'

def get_base_url():
    return 'https://api.trello.com/1/'

def get_api_key():
    return os.environ.get('TRELLO_API_KEY')

def get_api_token():
    return os.environ.get('TRELLO_API_TOKEN')

def get_board_id():
    return os.environ.get('TRELLO_BOARD_ID')


