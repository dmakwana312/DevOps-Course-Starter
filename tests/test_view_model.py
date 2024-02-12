from datetime import datetime

from freezegun import freeze_time

from todo_app.data.Item import Item
from todo_app.view_model import ViewModel
from todo_app.trello_config import TO_DO_LIST_NAME, DONE_LIST_NAME

def test_done_items_when_no_done_item():
    items = [
        Item(1, 'Task 1', datetime.now(), TO_DO_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 0

def test_done_items_when_done_item_exists():

    done_item=Item(2, 'Task 2', datetime.now(), DONE_LIST_NAME)

    items = [
        Item(1, 'Task 1', datetime.now(), TO_DO_LIST_NAME),
        done_item
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 2
    assert len(view_model.done_items) == 1
    assert view_model.done_items == [done_item]

def test_todo_items_when_no_todo_item_exist():
    items = [
        Item(1, 'Task 1', datetime.now(), DONE_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert len(view_model.todo_items) == 0

def test_todo_items_when_todo_item_exists():
    items = [
        Item(1, 'Task 1', datetime.now(), TO_DO_LIST_NAME),
        Item(2, 'Task 2', datetime.now(), DONE_LIST_NAME)
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 2
    assert len(view_model.todo_items) == 1
    assert all(view_model.todo_items) == all([Item(1, 'Task 1', datetime.now(), TO_DO_LIST_NAME)])

def test_view_model_status_not_from_possible_options():
    items = [
        Item(1, 'Task 1', datetime.now(), 'Random Status')
    ]

    view_model = ViewModel(items)
    
    assert len(view_model.items) == 1
    assert len(view_model.todo_items) == 0
    assert len(view_model.done_items) == 0

def test_view_model_should_show_all_done_items_when_no_items_done():
    items = []

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 0
    assert view_model.should_show_all_done_items


def test_view_model_should_show_all_done_items_when_3_items_done():
    items = [Item(i, 'Task', datetime.now(), DONE_LIST_NAME) for i in range(1, 4)]
    items.append(Item(10, 'Task', datetime.now(), TO_DO_LIST_NAME))

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 3
    assert view_model.should_show_all_done_items


def test_view_model_should_show_all_done_items_when_six_items_done():
    items = [Item(i, 'Task', datetime.now(), DONE_LIST_NAME) for i in range(1, 7)]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 6
    assert not view_model.should_show_all_done_items

@freeze_time("2023-01-01 12:00:00")
def test_view_model_recent_done_items_when_1_item_modified_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2022, 12, 31, 12, 00, 00), DONE_LIST_NAME),
        Item(2, 'Done Today', datetime(2023, 1, 1, 12, 00, 00), DONE_LIST_NAME),
        Item(3, 'Not Done', datetime(2023, 1, 1, 12, 00, 00), TO_DO_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert view_model.recent_done_items == [
        Item(2, 'Done Today', datetime(2023, 1, 1, 12, 00, 00), DONE_LIST_NAME)
    ]

@freeze_time("2023-01-01 12:00:00")
def test_view_model_old_done_items_when_1_item_modified_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2022, 12, 31, 12, 00, 00), DONE_LIST_NAME),
        Item(2, 'Done Today', datetime(2023, 1, 1, 12, 00, 00), DONE_LIST_NAME),
        Item(3, 'Not Done', datetime(2023, 1, 1, 12, 00, 00), TO_DO_LIST_NAME)
    ]

    view_model = ViewModel(items)

    assert view_model.older_done_items == [
        Item(1, 'Done Yesterday', datetime(2022, 12, 31, 12, 00, 00), DONE_LIST_NAME)
    ]