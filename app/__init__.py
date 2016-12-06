from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from util import assets
from app import views
from app import getdata

