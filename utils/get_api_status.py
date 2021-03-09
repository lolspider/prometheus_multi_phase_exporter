import requests
import json


def get_token(d_method, d_url, d_headers, d_data, d_parser, **kwargs):
    if d_method == "POST":
        try:
            r = requests.post(d_url, data=json.dumps(d_data), headers=d_headers, **kwargs)
            if 200 <= int(r.status_code) <= 299:
                token = json.loads(r.text)["%s" % d_parser]
                return token
            else:
                return False
        except Exception:
            return False


def fetch_response(method, url, headers, **kwargs):
    if method == "POST":
        try:
            r = requests.post(url, headers=headers, **kwargs)
            if 200 <= int(r.status_code) <= 299:
                api_status = 1
            else:
                api_status = 0
            return api_status
        except Exception:
            return 0

    try:
        r = requests.get(url, headers=headers)
        if 200 <= int(r.status_code) <= 299:
            api_status = 1
        else:
            api_status = 0
        return api_status
    except Exception:
        return 0


def get_key_api_status(url, headers):
    r = requests.get(url, headers)
    return r.status_code
