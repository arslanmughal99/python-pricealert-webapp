from flask import Blueprint, render_template

store_blueprint = Blueprint('store', __name__)


@store_blueprint.route('/')
def index():
    return render_template("stores/store_list.html")

@store_blueprint.route('/store/<string:name>')
def store_page():
    pass
