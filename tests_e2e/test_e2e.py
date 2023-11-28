import os
import pytest
from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from todo_app import app
from todo_app.data.Item import Item
from todo_app.data.trello_items import build_url, build_params, get_items
import requests

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load our real environment variables
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    # Give the app a moment to start
    sleep(1)

    # Return the application object as the result of the fixture
    yield application

    # Tear down
    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board():

    url = build_url('boards/?name=End To End Test Board')

    response = requests.post(url, params=build_params())
    response_json = response.json()
    return response_json['id']

def delete_trello_board(board_id):
    url = build_url('boards/' + os.environ['TRELLO_BOARD_ID'])

    requests.delete(url, params=build_params())

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=chrome_options) as driver:
        yield driver

@pytest.mark.order1
def test_task_journey_creation(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    input_text_box = driver.find_element("id", "to_do_title")
    input_text_box.send_keys('Task 1')

    create_button = driver.find_element(By.XPATH,'//button[text()="Create"]')
    create_button.click()

    sleep(1)

    item_id = get_item_id('Task 1');
    if item_id == None:
        pytest.fail('Item not created in Trello')
    else:
        assert check_element_exists_by_id(driver, item_id)
        assert not check_item_status(driver, item_id)

@pytest.mark.order2
def test_task_journey_mark_complete(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    item_id = get_item_id('Task 1');

    if item_id == None:
        pytest.fail('Item not created in Trello')

    item_checkbox = driver.find_element('id', 'status_' + item_id)
    item_checkbox.click()

    sleep(1)

    item_id = get_item_id('Task 1');
    
    assert check_element_exists_by_id(driver, item_id)
    assert check_item_status(driver, item_id)

@pytest.mark.order3
def test_task_journey_mark_incomplete(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    item_id = get_item_id('Task 1');
    if item_id == None:
        pytest.fail('Item not created in Trello')

    item_checkbox = driver.find_element('id', 'status_' + item_id)
    item_checkbox.click()

    sleep(1)

    item_id = get_item_id('Task 1');
    if item_id == None:
        pytest.fail('Item not created in Trello')

    assert check_element_exists_by_id(driver, item_id)
    assert not check_item_status(driver, item_id)

@pytest.mark.order4
def test_task_journey_mark_delete(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    
    item_id = get_item_id('Task 1');
    if item_id == None:
        pytest.fail('Item not created in Trello')
    
    delete_button = driver.find_element(By.XPATH,'//button[text()="Delete"]')
    delete_button.click()

    sleep(1)
    
    assert not check_element_exists_by_id(driver, item_id)

def check_item_status(driver, id):
    item_checkbox = driver.find_element('id', 'status_' + id)
    return item_checkbox.is_selected()

def get_item_id(name):
    items = get_items()
    for item in items:
        if item.name == name:
            return item.id
    return None

def check_element_exists_by_id(driver, id):
    try:
        driver.find_element('id', 'item_' + id)
    except NoSuchElementException:
        return False
    return True
