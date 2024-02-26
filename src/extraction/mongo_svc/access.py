"""This is the module that connects extraction service to the mongodb service.
"""

import requests

def store(config, data):
    """Store data to mongo db.

    Args:
        config: dictionary with config information.
        data: dictionary to be stored in mongodb, should follow the format as below
        {'keyword': keyword, 'news': [list of news dictionary]}

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    response = requests.post(
        f"http://{config['MONGO_SVC_ADDRESS']}/insert",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)