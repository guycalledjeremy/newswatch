"""This is the module within gateway service that accesses the auth service to login.
"""

import requests

def login(request, config):
    """Access login function from auth service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    auth = request.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basic_auth = (auth.username, auth.password)

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        f"http://{config['AUTH_SVC_ADDRESS']}/login", # look up at auth table
        auth=basic_auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)