"""This is the module that handles user news subscription.
"""

from flask import Flask, request

from .sql_svc import access
from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = config_utils.load_config("auth/config.yaml")

@server.route("/subscribe", methods=["POST"])
def subscribe():
    """Subscribe a new keyword to the news watchlist.

    Returns:
        A tuple, A message and a status code.
    """
    msg, err = access.insert(request, config)

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
    msg, err = access.delete(request, config)

    if not err:
        return msg, 200
    else:
        return err

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000, debug=True)