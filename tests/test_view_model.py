from todo_app.data.Item import Item
from todo_app.view_model import ViewModel

from todo_app.data.trello_config import TO_DO_LIST_NAME, DONE_LIST_NAME

def test_done_items_when_no_done_item():
    items = [
        Item(1, 'Task 1', TO_DO_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 0

def test_done_items_when_done_item_exists():
    items = [
        Item(1, 'Task 1', TO_DO_LIST_NAME),
        Item(2, 'Task 2', DONE_LIST_NAME)
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 2
    assert len(view_model.done_items) == 1
    assert view_model.done_items == [Item(2, 'Task 2', DONE_LIST_NAME)]

def test_todo_items_when_no_todo_item_exist():
    items = [
        Item(1, 'Task 1', DONE_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert len(view_model.todo_items) == 0

def test_todo_items_when_todo_item_exists():
    items = [
        Item(1, 'Task 1', TO_DO_LIST_NAME),
        Item(2, 'Task 2', DONE_LIST_NAME)
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 2
    assert len(view_model.todo_items) == 1
    assert view_model.todo_items == [Item(1, 'Task 1', TO_DO_LIST_NAME)]

def test_view_model_status_not_from_possible_options():
    items = [
        Item(1, 'Task 1', 'Random Status')
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 1
    assert len(view_model.todo_items) == 0
    assert len(view_model.done_items) == 0
    