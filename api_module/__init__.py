from flask import Flask
import os

from .models import init_db

app = Flask(__name__)
db_adress = f"{os.environ['BASE_DB_URL']}{os.environ['DB_PORTS']}{os.environ['DB_NAME']}"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_adress

init_db(app)


from . import routes

