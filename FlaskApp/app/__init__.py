from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
POSTGRES = {
    'user': 'postgres',
    'pw': '123456',
    'db': 'userdatabase',
    'host': 'localhost',
    'port': '5432',
}
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
login_manager = LoginManager(app)
from app.controllers import main_controllers,post_controllers,user_controllers
