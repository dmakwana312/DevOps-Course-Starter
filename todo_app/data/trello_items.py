import requests

def build_params(additional_params = {}):
    default_params = { 'key': '062e02a471e570c709c77f10f1249e0f', 'token': 'ATTA8ac5a77f612d898fbb18d09b18fe237fabe01e6a306d151a773307df920dbd42624E5C0F' }
    default_params.update(additional_params)
    return default_params

def get_items():
    url = 'https://api.trello.com/1/boards/64f5c617d9a26e50962586f6/lists?cards=open'
    response = requests.get(url, params=build_params())
    response_json = response.json()

    items = []

    for list in response_json:
        if list['cards'] != []:
            for card in list['cards']:
                items.append( { 'id': card['id'], 'status': 'Complete' if list['name'] == 'Done' else "Not Started" , 'title': card['name'] })

    return items

def get_lists():
    url = 'https://api.trello.com/1/boards/64f5c617d9a26e50962586f6/lists'
    response = requests.get(url, params=build_params())
    return response.json()

def get_list_id(name):
    all_lists = get_lists()

    for list in all_lists:
        if list['name'] == name:
            return list['id']

    return None
    

def mark_complete(id):
    done_list_id = get_list_id('Done')
    url = 'https://api.trello.com/1/cards/' + id
    response = requests.put(url, params=build_params({ 'idList':  done_list_id }))
    return response.status_code == 200

def mark_incomplete(id):
    to_do_list_id = get_list_id('To Do')
    url = 'https://api.trello.com/1/cards/' + id
    response = requests.put(url, params=build_params({ 'idList':  to_do_list_id }))
    return response.status_code == 200

def delete_item(id):
    url = 'https://api.trello.com/1/cards/' + id
    response = requests.delete(url, params=build_params())
    return response.status_code == 200

def add_item(name):
    to_do_list_id = get_list_id('To Do')
    url = 'https://api.trello.com/1/cards/'
    response = requests.post(url, params=build_params({ 'idList':  to_do_list_id, 'name': name }))
    return response.status_code == 200


