"""
"""

import requests

def login():
    """Access login function from auth service through POST.
    """
    basic_auth = ("admin", "Admin123")
    # basic_auth = ("admin", "Admin12")
    # basic_auth = ("admi", "Admin123")

    # post auth info to login function from auth service, if successful, response
    # should contain an encoded jwt.
    response = requests.post(
        "http://localhost:3060/lookup/aut",
        auth=basic_auth
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

if __name__ == "__main__":
    print(login())