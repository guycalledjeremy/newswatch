"""This is the module that handles user news subscription.
"""

from flask import Flask, request

from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = config_utils.load_config("auth/config.yaml")

@server.route("/subscribe", methods=["POST"])
def subscribe():
    pass