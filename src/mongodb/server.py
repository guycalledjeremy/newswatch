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

@server.route("/lookup/<keyword>", methods=["POST"])
def lookup(keyword):
    """look up all news related to one keyword.
    """
    try:
        collection = mongo.db[keyword]
        documents = list(collection.find({}))
        for doc in documents:
            doc['_id'] = str(doc['_id'])

        if len(documents) != 0:
            return jsonify({'message': 'successful lookup', 'documents': documents}), 200
        else:
            return jsonify({'message': 'keyword not found'}), 404
    except Exception as err:
        return jsonify({'message': str(err)}), 500

@server.route("/insert", methods=["POST"])
def insert():
    """insert a row to a given table.
    """
    data = request.get_json()

    try:
        mongo.db[data["keyword"]].insert_many(data["news"])
        return jsonify({'message': 'successful insert'}), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 500

@server.route("/delete/<keyword>", methods=["POST"])
def delete(keyword):
    """delete all news related to one keyword.
    """
    try:
        collection = mongo.db[keyword]

        # make sure the collection related to the given keyword is not empty
        if collection.count_documents({}) == 0:
            return jsonify({'message': 'keyword not found'}), 404

        collection.drop()

        return jsonify({'message': f'successful delete keyword "{keyword}"'}), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 500

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=9000, debug=True)