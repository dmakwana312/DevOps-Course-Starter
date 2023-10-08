from todo_app.trello_config import TO_DO_LIST_NAME, DONE_LIST_NAME

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
    
    @property
    def should_show_all_done_items(self):
        return len(self.done_items) < 5
    
    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.modified_today()]
    
    @property
    def older_done_items(self):
        return [item for item in self.done_items if not item.modified_today()]