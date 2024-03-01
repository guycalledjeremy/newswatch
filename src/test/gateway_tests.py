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
        "http://newswatch.com/login",
        auth=basic_auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def subscribe(jwt):
    """placeholder for old test code.
    """
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    data = {
        'username': 'admin',
        'keyword': 'apple'
    }

    response = requests.post(
        "http://newswatch.com/subscribe",
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def unsubscribe(jwt):
    """placeholder for old test code.
    """
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    data = {
        'username': 'admin',
        'keyword': 'apple'
        # 'keyword': 'google'
    }

    response = requests.post(
        "http://newswatch.com/unsubscribe",
        json=data,
        headers=headers
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

if __name__ == "__main__":
    ### Tests for auth
    jwt, err = login()
    print(jwt, err)

    ### Tests for subscription
    print(subscribe(jwt))
    print(unsubscribe(jwt))