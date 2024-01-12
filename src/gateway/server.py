"""This is the module that acts as gateway for requests from the client and other services.
"""

import datetime, json

from flask import Flask, request

from .auth_svc import access, validate
from .sub_svc import update
from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = config_utils.load_config("gateway/config.yaml")

@server.route("/login", methods=["POST"])
def login():
    """Log registered users in and assigns jwt.

    Returns:
        A tuple, An encoded jwt/error message and a status code.
    """
    token, err = access.login(request, config)

    if not err:
        return token, 200
    else:
        return err

@server.route("/subscribe", methods=["POST"])
def subscribe():
    """Subscribe user to a news keyword.

    Returns:
        A tuple, A result message and a status code.
    """
    access, err = validate.token(request, config)

    if err:
        return err
    
    # access here is the jwt dictionary encoded by the auth service for the user/client
    access = json.loads(access)
    if not access["admin"]:
        return "not authorized", 401
    elif datetime.datetime.fromtimestamp(access["exp"]) < datetime.datetime.utcnow():
        return "login expired", 401
    else:
        msg, err = update.subscribe(request, config)

        if not err:
            return msg, 200
        else:
            return err

@server.route("/unsubscribe", methods=["POST"])
def unsubscribe():
    """Unsubscribe user to a news keyword.

    Returns:
        A tuple, A result message and a status code.
    """
    access, err = validate.token(request, config)

    if err:
        return err
    
    # access here is the jwt dictionary encoded by the auth service for the user/client
    access = json.loads(access)
    if not access["admin"]:
        return "not authorized", 401
    elif datetime.datetime.fromtimestamp(access["exp"]) < datetime.datetime.utcnow():
        return "login expired", 401
    else:
        msg, err = update.unsubscribe(request, config)

        if not err:
            return msg, 200
        else:
            return err

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)