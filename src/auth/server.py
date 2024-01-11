"""This is the module that handles user authentification and sends out jwt.
"""

import datetime

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

    Returns:
        An encoded jwt or errror message
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

@server.route("/validate", methods=["POST"])
def validate():
    """Decode jwt for validation.

    Returns:
        A tuple, A decoded jwt/error message and a status code.
    """
    encoded = request.headers["Authorization"]

    if not encoded:
        return "missing credentials", 401

    head, encoded = map(str.strip, encoded.split(' '))
    if head != "Bearer":
        return "invalid Authorization type", 401
    try:
        decoded = jwt.decode(
            encoded, secret["JWT_SECRET"], algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200

def createJWT(username, secret, authz):
    """Create and encode a JWT for a registered user as identification..

    Returns:
        An encoded jwt.
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