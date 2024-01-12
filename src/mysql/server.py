"""This is the module that works with the sql database.
"""

from flask import Flask, request
from flask_mysqldb import MySQL

from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)
mysql = MySQL(server)

# config
config = config_utils.load_config("mysql/config.yaml")
server.config["MYSQL_HOST"] = config['MYSQL_HOST']
server.config["MYSQL_USER"] = config['MYSQL_USER']
server.config["MYSQL_DB"] = config['MYSQL_DB']
server.config["MYSQL_PORT"] = int(config['MYSQL_PORT'])
# secret config
secret = config_utils.load_config("mysql/secret.yaml")
server.config["MYSQL_PASSWORD"] = secret['MYSQL_PASSWORD']

def lookup_auth(auth):
    """Helper function to look up auth table.

    Args:
        auth: A dictionary with authentification information passed in through post request.

    Returns:
        A tuple, a string indicating whether the given data is found in the table and a status code.
    """
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT username, passcode FROM user WHERE username=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone() # user_row = [username, password]
        username = user_row[0]
        password = user_row[1]

        if auth.username != username or auth.password != password:
            return "invalid", 401
        else:
            return "found", 200
    else: # when the credentials are not found in auth
        return "not found", 401

def lookup_subscription(username, keyword):
    """Helper function to look up subscription table.

    Args:
        username: A string that is the name of the user.
        keyword: A string that is the keyword to be subscribed.

    Returns:
        A tuple, a string indicating whether the given data is found in the table and a status code.
    """
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT username, keyword FROM subscription WHERE username = %s AND keyword = %s", (username, keyword)
    )

    if res > 0:
        return "found", 200
    else:
        return "not found", 401

@server.route("/lookup/<table>", methods=["POST"])
def lookup(table):
    """look up information in a specified table from the database.

    Args:
        table: A string that is the name of the table to look up from.

    Returns:
        A tuple, a string indicating whether the given data is found in the table and a status code.
    """
    if table == "auth":
        return lookup_auth(request.authorization)
    else:
        return "invalid lookup table", 404

def insert_subscription(username, keyword):
    """Helper function to insert row to subscription table.

    Args:
        username: A string that is the name of the user.
        keyword: A string that is the keyword to be subscribed.

    Returns:
        A tuple, a response message and a status code.
    """
    cur = mysql.connection.cursor()

    try:
        cur.execute(
            "INSERT INTO subscription(username, keyword) VALUES (%s, %s)", (username, keyword)
        )
        mysql.connection.commit()

        affected_rows = cur.rowcount
        if affected_rows > 0:
            return "successful insert", 200
        else:
            return "unsuccessful insert", 500
    except mysql.connection.Error as err:
        return str(err), 500

@server.route("/insert/<table>", methods=["POST"])
def insert(table):
    """insert a row to a given table.
    """
    if table == "subscription":
        data = request.get_json()
        return insert_subscription(data.get('username'), data.get('keyword'))
    else:
        return "invalid table to insert", 404

def delete_subscription(username, keyword):
    """Helper function to delete row from subscription table.

    Args:
        username: A string that is the name of the user.
        keyword: A string that is the keyword to be subscribed.

    Returns:
        A tuple, a response message and a status code.
    """
    cur = mysql.connection.cursor()
    
    # check if row exists
    _, code = lookup_subscription(username, keyword)
    if code == 200:
        try:
            cur.execute(
                "DELETE FROM subscription WHERE username = %s AND keyword = %s", (username, keyword)
            )
            mysql.connection.commit()

            affected_rows = cur.rowcount
            if affected_rows > 0:
                return "successful delete", 200
            else:
                return "unsuccessful delete", 500
        except mysql.connection.Error as err:
            return str(err), 500
    else:
        return f"trying to delete non-existent keyword: {keyword}", code

@server.route("/delete/<table>", methods=["POST"])
def delete(table):
    """delete a row from a given table.
    """
    if table == "subscription":
        data = request.get_json()
        return delete_subscription(data.get('username'), data.get('keyword'))
    else:
        return "invalid table to delete", 404

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=3060, debug=True)