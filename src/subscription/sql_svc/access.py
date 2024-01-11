import requests

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
        "http://localhost:3060/insert/subscription",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

if __name__ == "__main__":
    print(subscribe())