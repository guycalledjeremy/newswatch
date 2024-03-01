"""This is the module that handles user news subscription.
"""

import os

from flask import Flask, request

from sql_svc import modify
# from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = {"SQL_SVC_ADDRESS": os.environ.get("SQL_SVC_ADDRESS")}
# config = config_utils.load_config("subscription/config.yaml")

@server.route("/subscribe", methods=["POST"])
def subscribe():
    """Subscribe a new keyword to the news watchlist.

    Returns:
        A tuple, A message and a status code.
    """
    msg, err = modify.insert(request, config)

    if not err:
        return msg, 200
    else:
        return err

@server.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    """Unsubscribe a keyword from the news watchlist.

    Returns:
        A tuple, A message and a status code.
    """
    msg, err = modify.delete(request, config)

    if not err:
        return msg, 200
    else:
        return err

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000, debug=True)