from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nvmeevmvuszlwq:9bc4228671430435b1a64d5003a4f59661c05f018ba22bd1e20c6cc82f11b050@ec2-3-226-165-146.compute-1.amazonaws.com:5432/df536mu06jkfig'
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
db = SQLAlchemy(app)

