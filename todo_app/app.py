from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item, delete_item

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=sorted(get_items(), key=lambda k : k['status'], reverse=True))

@app.route('/addToDo', methods=['POST'])
def add_to_do():
    add_item(request.form.get('to_do_title'))
    return redirect('/')

@app.route('/markComplete', methods=['POST'])
def markComplete():
    item_id = request.form.get('itemId')
    item_status = request.form.get('status')

    todo_item = get_item(item_id)
    status = None
    if item_status == 'true':
        status = 'Complete'
    else:
        status = 'Not Started' 

    todo_item['status'] = status
    save_item(todo_item)

    return '', 200

@app.route('/deleteItem', methods=['POST'])
def deleteItem():
    item_id = request.form.get('itemId')
    
    delete_item(item_id)

    return '', 200
