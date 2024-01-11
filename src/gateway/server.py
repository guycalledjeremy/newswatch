import requests

def login():
    """placeholder for old test code.
    """
    basic_auth = ("admin", "Admin123")
    # basic_auth = ("admin", "Admin12")
    # basic_auth = ("admi", "Admin123")

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        "http://localhost:5000/login",
        auth=basic_auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def validate(jwt):
    """placeholder for old test code.
    """
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        "http://localhost:5000/validate",
        headers=headers
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def subscribe():
    """placeholder for old test code.
    """
    data = {
        'username': 'admin',
        'keyword': 'apple'
    }

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        "http://localhost:8000/subscribe",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def unsubscribe():
    """placeholder for old test code.
    """
    data = {
        'username': 'admin',
        'keyword': 'apple'
        # 'keyword': 'google'
    }

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        "http://localhost:8000/unsubscribe",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

if __name__ == "__main__":
    ### Tests for auth
    # jwt, err = login()
    # print(jwt, err)

    # print(validate(jwt))

    ### Tests for subscription
    print(subscribe())
    print(unsubscribe())