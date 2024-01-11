import requests

def insert(request, config):
    """Insert a row to subscription table using mysql service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    request_json = request.get_json()
    if "username" in request_json and "keyword" in request_json:
        data = {
            "username": request_json["username"],
            "keyword": request_json["keyword"]
        }
    else:
        return "bad request: missing keyword", 400

    response = requests.post(
        f"http://{config['SQL_SVC_ADDRESS']}/insert/subscription",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def delete(request, config):
    """Delete a row to subscription table using mysql service through POST.

    Args:
        request: flask post request.
        config: dictionary with config information.

    Returns:
        If request processed successfully, return response and None as a tuple; if request not
    processed successfully, return None and (error text, error status code) as a tuple.
    """
    request_json = request.get_json()
    if "username" in request_json and "keyword" in request_json:
        data = {
            "username": request_json["username"],
            "keyword": request_json["keyword"]
        }
    else:
        return "bad request: missing keyword", 400

    response = requests.post(
        f"http://{config['SQL_SVC_ADDRESS']}/delete/subscription",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)