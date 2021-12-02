import os
import  json
from time import sleep

import redis
from flask import Flask, request


app = Flask(__name__)


@app.route("/")
def index():
    return 'Test'
