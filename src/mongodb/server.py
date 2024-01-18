"""This is the module that works with the mongo database.
"""

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

from common import config_utils

# configures Flask server and mysql database
server = Flask(__name__)

# config
server.config["MONGO_URI"] = "mongodb://localhost:27017/news"
config = config_utils.load_config("mongodb/config.yaml")
# secret config
secret = config_utils.load_config("mongodb/secret.yaml")

mongo = PyMongo(server)

@server.route("/insert", methods=["POST"])
def insert():
    """insert a row to a given table.
    """
    data = request.get_json()

    try:
        res = mongo.db[data["keyword"]].insert_one(data["news"])
        return jsonify({'message': 'successful insert', 'id': str(res.inserted_id)}), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 500

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=9000, debug=True)