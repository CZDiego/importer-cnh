import requests
import json

class HttpClient(object):
    def get(url):
        r = requests.get(url)
        return r.json() if r.status_code == requests.codes.ok else r.text

    def post(url, payload):
       headers={'Content-type':'application/json', 'Accept':'application/json'}
       r = requests.post(url, json=payload, headers=headers)
       return r.json() if r.status_code == requests.codes.ok else r.text
