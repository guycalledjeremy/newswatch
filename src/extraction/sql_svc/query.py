"""This is the module that connects extraction service to the mySQL service.
"""

import json, requests

def get_keywords(config):
    """Get all keywords amongst all users from the sql database.

    Args:
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    response = requests.post(
        f"http://{config['SQL_SVC_ADDRESS']}/query"
    )

    if response.status_code == 200:
        return json.loads(response.text), None
    else:
        return None, (response.text, response.status_code)