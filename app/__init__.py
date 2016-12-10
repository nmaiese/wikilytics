from flask import Flask
from flask_compress import Compress

app = Flask(__name__)
app.config.from_object('config')
Compress(app)

from util import assets
from app import views
from app import getdata

