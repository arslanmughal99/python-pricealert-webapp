from flask import Flask, render_template
from common.database import Database


#Configuring Flask
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "5422"

#this method run function before all the requests
@app.before_first_request
def init_db():
    Database.initialize()

@app.route("/")
def home():
    return render_template("home.html")



# registering blueprint for users
from models.alerts.views import alert_blueprint
from models.stores.views import store_blueprint
from models.users.views import user_blueprint
app.register_blueprint(store_blueprint, url_prefix="/store")
app.register_blueprint(alert_blueprint, url_prefix="/alert")
app.register_blueprint(user_blueprint, url_prefix="/users")

























