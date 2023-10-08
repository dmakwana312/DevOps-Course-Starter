from dotenv import load_dotenv, find_dotenv
from todo_app import app

import pytest
import requests
import os

mocked_items = {'to_do_items': [{'id': '123', 'name': 'Test card', 'dateLastActivity': '2023-01-01T12:00:00.000Z'}], 'done_items': []}

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

class StubResponse():
    def __init__(self, fake_response_data, ok=True):
        self.fake_response_data = fake_response_data
        self.ok = ok
        
    def json(self):
        return self.fake_response_data
    

def stub(url, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists?cards=open':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': mocked_items['to_do_items']
        },
        {
            'id': '456def',
            'name': 'Done',
            'cards': mocked_items['done_items']
        }]
        return StubResponse(fake_response_data)
    
    elif url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [
            {
                'id': '123abc',
                'name': 'To Do',
            },
            {
                'id': '456def',
                'name': 'Done',
            }]
        return StubResponse(fake_response_data)
    
    elif url == f'https://api.trello.com/1/cards/':
        mocked_items['to_do_items'].append({'id': '456', 'name': 'Created in Integration Test', 'dateLastActivity': '2023-01-01T12:00:00.000Z',})
        fake_response_data = {
            'id': '456', 
            'name': 'Created in Integration Test',
            'idList': '123abc',
            'dateLastActivity': '2023-01-01T12:00:00.000Z'
        }
        return StubResponse(fake_response_data)
    
    elif url == f'https://api.trello.com/1/cards/456':

        if params.get('idList') == None:
            mocked_items['to_do_items'].pop()
            return StubResponse({})
        
        elif params['idList'] == '456def':
            completedItem = mocked_items['to_do_items'].pop()
            mocked_items['done_items'].append(completedItem)
            fake_response_data = {
                'id': '456', 
                'name': 'Created in Integration Test',
                'idList': params['idList'],
                'dateLastActivity': '2023-01-01T12:00:00.000Z',
            }
            return StubResponse(fake_response_data)
        
        elif params['idList'] == '123abc':
            incompleteItem = mocked_items['done_items'].pop()
            mocked_items['to_do_items'].append(incompleteItem)
            fake_response_data = {
                'id': '456', 
                'name': 'Created in Integration Test',
                'idList': params['idList'],
                'dateLastActivity': '2023-01-01T12:00:00.000Z',
            }
            return StubResponse(fake_response_data)

    raise Exception(f'Integration test did not expect URL "{url}"')

@pytest.mark.order1
def test_index_page(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    response = client.get('/')

    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
    assert 'To Do Items' in response.data.decode()
    assert 'Done Items' in response.data.decode()

@pytest.mark.order2
def test_add_item(monkeypatch, client):
    
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'post', stub)
    response = client.post('/addToDo', data={'to_do_title': 'Created in Integration Test'})

    assert response.status_code == 302

    response = client.get('/')
    
    assert 'Test card' in response.data.decode()
    assert 'To Do Items' in response.data.decode()
    assert 'Done Items' in response.data.decode()
    assert 'Created in Integration Test' in response.data.decode()

@pytest.mark.order3
def test_mark_item_complete(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'put', stub)
    response = client.post('/complete_item', data={'itemId': '456', 'status': 'true'})

    assert response.status_code == 201

    response = client.get('/')
    
    assert 'Test card' in response.data.decode()
    assert 'To Do Items' in response.data.decode()
    assert 'Done Items' in response.data.decode()
    assert 'Created in Integration Test' in response.data.decode()
    assert 'id="status_456"  checked' in response.data.decode()

@pytest.mark.order4
def test_mark_item_incomplete(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'put', stub)
    response = client.post('/complete_item', data={'itemId': '456', 'status': 'false'})

    assert response.status_code == 201

    response = client.get('/')
    
    assert 'Test card' in response.data.decode()
    assert 'To Do Items' in response.data.decode()
    assert 'Done Items' in response.data.decode()
    assert 'Created in Integration Test' in response.data.decode()
    assert 'id="status_456"  checked' not in response.data.decode()

@pytest.mark.order5
def test_delete_items(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)
    monkeypatch.setattr(requests, 'delete', stub)
    response = client.post('/deleteItem', data={'itemId': '456'})

    assert response.status_code == 201

    response = client.get('/')
    
    assert 'Test card' in response.data.decode()
    assert 'To Do Items' in response.data.decode()
    assert 'Done Items' in response.data.decode()
    assert 'Created in Integration Test' not in response.data.decode()
   