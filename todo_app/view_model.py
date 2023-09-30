from todo_app.data.trello_config import TO_DO_LIST_NAME, DONE_LIST_NAME

class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def todo_items(self):
        return [item for item in self.items if item.status == TO_DO_LIST_NAME]

    @property
    def done_items(self):
        return [item for item in self.items if item.status == DONE_LIST_NAME]
    
    