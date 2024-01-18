import requests

def add_news():
    """
    """
    data = {
        'keyword': 'apple',
        'news': {
            'test key': 'test value'
        }
    }

    response = requests.post(
        "http://localhost:9000/insert",
        json=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def lookup_news(keyword):
    """
    """
    response = requests.post(
        f"http://localhost:9000/lookup/{keyword}"
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

if __name__ == "__main__":
    # print(add_news())
    print(lookup_news('apple'))
    print(lookup_news('google'))