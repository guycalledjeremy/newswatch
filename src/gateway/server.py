"""This is the module that acts as gateway for requests from the client and other services.
"""

from flask import Flask, request

from .auth_svc import access
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

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)