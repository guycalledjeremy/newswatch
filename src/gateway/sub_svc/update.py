"""This is the module within gateway service that accesses the subscriptoin service for subscribe and unsubscribe.
"""

import requests

def subscribe(request, config):
    """Access subscribe function from subscription service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    response = requests.post(
        f"http://{config['SUB_SVC_ADDRESS']}/subscribe",
        json=request.get_json()
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def unsubscribe(request, config):
    """Access subscribe function from subscription service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    response = requests.post(
        f"http://{config['SUB_SVC_ADDRESS']}/unsubscribe",
        json=request.get_json()
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)