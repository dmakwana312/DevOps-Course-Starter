from datetime import date, datetime


class Item:
    def __init__(self, id, name, last_modified, status = 'To Do', ):
        self.id = id
        self.name = name
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ'), list['name'])
    
    def modified_today(self):
        return self.last_modified.date() == date.today()

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False

        return self.id == other.id  and self.name == other.name and self.status == other.status and self.last_modified == other.last_modified