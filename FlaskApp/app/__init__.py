from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

app = Flask(__name__)
POSTGRES = {
'user': 'postgres',
'pw': '123456',
'db': 'flaskapp',
'host': 'localhost',
'port': '5432',
}
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'phamvietdaoit@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'phamvietdaoit@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = '01667781178' # enter your password here
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#config postgresql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
#config email
mail = Mail(app)
login_manager = LoginManager(app)
from app.controllers import main_controllers,post_controllers,user_controllers
