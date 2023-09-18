import requests
import todo_app.data.trello_config as config

def build_url(endpoint):
    return config.BASE_URL + endpoint

def build_params(additional_params = {}):
    default_params = { 'key': config.API_KEY, 'token': config.API_TOKEN }
    default_params.update(additional_params)
    return default_params

def get_items():
    url = build_url('boards/' + config.BOARD_ID + '/lists?cards=open')
    response = requests.get(url, params=build_params())
    response_json = response.json()

    items = []

    for list in response_json:
        if list['cards'] != []:
            for card in list['cards']:
                items.append( { 'id': card['id'], 'status': 'Complete' if list['name'] == config.DONE_LIST_NAME else "Not Started" , 'title': card['name'] })

    return items

def get_lists():
    url = build_url('boards/' + config.BOARD_ID + '/lists')
    response = requests.get(url, params=build_params())
    return response.json()

def get_list_id(name):
    all_lists = get_lists()

    for list in all_lists:
        if list['name'] == name:
            return list['id']

    return None
    

def mark_complete(id):
    done_list_id = get_list_id(config.DONE_LIST_NAME)
    url = build_url('cards/' + id)
    response = requests.put(url, params=build_params({ 'idList':  done_list_id }))
    return response.status_code == 200

def mark_incomplete(id):
    to_do_list_id = get_list_id(config.TO_DO_LIST_NAME)
    url = build_url('cards/' + id)
    response = requests.put(url, params=build_params({ 'idList':  to_do_list_id }))
    return response.status_code == 200

def delete_item(id):
    url = build_url('cards/' + id)
    response = requests.delete(url, params=build_params())
    return response.status_code == 200

def add_item(name):
    to_do_list_id = get_list_id(config.TO_DO_LIST_NAME)
    url = build_url('cards/')
    response = requests.post(url, params=build_params({ 'idList':  to_do_list_id, 'name': name }))
    return response.status_code == 200


