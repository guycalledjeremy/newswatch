"""This is the module that handles user authentification and sends out jwt.
"""

import datetime, os

import jwt
from flask import Flask, request

from .sql_svc import access
from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
config = config_utils.load_config("auth/config.yaml")
# secret config
secret = config_utils.load_config("auth/secret.yaml")

@server.route("/login", methods=["POST"])
def login():
    """Log registered users in and assigns jwt.
    """
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)

    # TODO: pass auth to sql svc and handle the returned response
    _, err = access.lookup(request, config)

    if not err:
        return createJWT(auth.username, secret["JWT_SECRET"], True) # login as admin by default
    else:
        return err

def createJWT(username, secret, authz):
    """Create and encode a JWT for a registered user as identification
    """
    return jwt.encode(
        {
            "username": username,
            # pct = utc - 8hr
            # exp = iat + 24hr
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=16),
            "iat": datetime.datetime.utcnow() - datetime.timedelta(hours=8),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)