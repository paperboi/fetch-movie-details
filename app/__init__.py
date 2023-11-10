from flask import Flask
from logging import FileHandler,WARNING

app = Flask(__name__, template_folder="templates")
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

from app import routes
