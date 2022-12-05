# Import from Python:
import requests

def save_result(data_json, url):

    # POST request to API to store data in Redis stream:
    try:
        rq = requests.post(url, json=data_json)
        return rq.text # Returns the id of the result in Redis stream

    except Exception as e:
        print(str(e))
        return ""
    