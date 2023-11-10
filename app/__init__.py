from flask import Flask
from logging import FileHandler,WARNING

app = Flask(__name__, template_folder="templates")

from app import routes
