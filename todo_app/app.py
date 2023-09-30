from flask import Flask, render_template, redirect, request

from todo_app.flask_config import Config
from todo_app.data.trello_items import get_items, add_item, mark_complete, mark_incomplete, delete_item
from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        item_view_model = ViewModel(sorted(get_items(), key=lambda k : k.status, reverse=True))
        return render_template('index.html', view_model=item_view_model)

    @app.route('/addToDo', methods=['POST'])
    def add_to_do():
        add_item(request.form.get('to_do_title'))
        return redirect('/')

    @app.route('/complete_item', methods=['POST'])
    def complete_item():
        item_id = request.form.get('itemId')
        item_status = request.form.get('status')
        success = mark_complete(item_id) if item_status == 'true' else mark_incomplete(item_id)
        return '', get_response_code(success)

    @app.route('/deleteItem', methods=['POST'])
    def deleteItem():
        item_id = request.form.get('itemId')
        success = delete_item(item_id)
        return '', get_response_code(success)

    def get_response_code(success):
        if success:
            return 200
        else:
            return 500
        
    return app