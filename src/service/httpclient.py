import requests
import json

class HttpClient(object):
    def get(url):
        r = requests.get(url)
        return r.json() if r.status_code == requests.codes.ok else r.text

    def post(url, payload):
       r = requests.post(url, data=payload)
       return r.json() if r.status_code == requests.codes.ok else r.text
