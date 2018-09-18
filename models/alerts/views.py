from flask import Blueprint, render_template, request, session, redirect, url_for
from models.alerts.alert import Alert
from models.items.item import Item
from models.users.decorator import requires_login
from common.database import Database

alert_blueprint = Blueprint('alert', __name__)




@requires_login
@alert_blueprint.route('/deactivate/<string:alert_id>')
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('user.user_alerts'))


@requires_login
@alert_blueprint.route('/activate/<string:alert_id>')
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('user.user_alerts'))


@requires_login
@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).remove()
    return redirect(url_for('user.user_alerts'))



@alert_blueprint.route("/new", methods=['GET', 'POST'])
def create_alert():
    if request.method == "POST":
        item_name = request.form['item_name']
        item_url = request.form['item_url']
        price_limit = request.form['price_limit']
        item = Item(str(item_name), str(item_url))
        item.save_to_mongo()
        alert = Alert(session['email'],price_limit, item._id)
        alert.load_item_price()  # this is already saving to mongodb
        return redirect(url_for('user.user_alerts'))
    return render_template("alerts/create_alert.html")

@alert_blueprint.route("/edit_alerts/<string:alert_id>", methods=['GET','POST'])
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == "POST":
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for("user.user_alerts"))
    return render_template("alerts/edit_alert.html",alert=alert)

@alert_blueprint.route('/<string:alert_id>')
@requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template("alerts/alert.html", alert=alert)





