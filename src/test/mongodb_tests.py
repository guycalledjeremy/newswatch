import json, requests

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
        return json.loads(response.text), None
    else:
        return None, (json.loads(response.text), response.status_code)

def lookup_news(keyword):
    """
    """
    response = requests.post(
        f"http://localhost:9000/lookup/{keyword}"
    )

    if response.status_code == 200:
        return json.loads(response.text), None
    else:
        return None, (json.loads(response.text), response.status_code)

def delete_news(keyword):
    """
    """
    response = requests.post(
        f"http://localhost:9000/delete/{keyword}"
    )

    if response.status_code == 200:
        return json.loads(response.text), None
    else:
        return None, (json.loads(response.text), response.status_code)

if __name__ == "__main__":
    # test for add
    print(add_news())

    # tests for lookup
    print(lookup_news('apple'))
    print(lookup_news('google'))

    # tests for delete
    print(delete_news('apple'))
    print(delete_news('google'))
    print(lookup_news('apple'))