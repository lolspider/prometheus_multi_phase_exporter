import requests
import json


def get_token(d_method, d_url, d_headers, d_data, d_parser, **kwargs):
    if d_method == "POST":
        r = requests.post(d_url, data=d_data, headers=d_headers, **kwargs)
        print(r.status_code, r.text)
        if 200 <= int(r.status_code) <= 299:
            token = json.loads(r.text)["%s" % d_parser]
            return token
        else:
            return False


def fetch_response(method, url, headers, **kwargs):
    if method == "POST":
        r = requests.post(url, headers=headers, **kwargs)
        if 200 <= int(r.status_code) <= 299:
            api_status = 1
        else:
            api_status = 0
        return api_status

    r = requests.get(url, headers=headers)
    if 200 <= int(r.status_code) <= 299:
        api_status = 1
    else:
        api_status = 0
    return api_status


def get_key_api_status(url, headers):
    r = requests.get(url, headers)
    return r.status_code
