"""This is the module within gateway service that accesses the auth service for validation.
"""

import requests

def token(request, config):
    """Access login function from auth service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    response = requests.post(
        f"http://{config['AUTH_SVC_ADDRESS']}/validate",
        headers=request.headers
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)