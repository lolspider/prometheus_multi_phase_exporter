import prometheus_client
import yaml
import json
from utils.get_api_status import *
from utils.custom_collector import *
from flask import Response, Flask
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

app = Flask(__name__)


@app.route("/health")
def health_check():
    return Response("OK")


@app.route("/metrics")
def response():
    for key, value in config["global"]["task"].items():
        # for 2p_api_request
        if '2p_api_request' in value:
            phase1 = value["2p_api_request"]["phase1"]
            # global phase2
            phase2 = value["2p_api_request"]["phase2"]

            if phase1["auth_type"] == "OAUTH2":
                token = get_token(phase1['method'], phase1['url'], phase1['headers'], urlencode(phase1['body']),
                                  phase1['token_parser'], auth=HTTPBasicAuth(phase1['username'],
                                                                             phase1['password']))
            else:
                token = get_token(phase1['method'], phase1['url'], phase1['headers'], json.dumps(phase1['body']),
                                  phase1['token_parser'])

            if token:
                phase2['headers']['Authorization'] = 'Bearer {}'.format(token)
                if phase2["method"] == "POST":
                    result.update({key: fetch_response(phase2["method"], phase2["url"], headers=phase2['headers'],
                                                       data=json.dumps(phase2['body']))})
                else:
                    result.update({key: fetch_response(phase2["method"], phase2["url"], headers=phase2['headers'])})
            else:
                result.update({key: 0})

        # for other modules
        else:
            exit(1)
    if "integration_api" in phase2.keys():
        return Response(prometheus_client.generate_latest(CustomCollector("up", "monitor api status", ["integration"],
                                                                          result)), mimetype="text/plain")
    else:
        return Response(prometheus_client.generate_latest(CustomCollector("up", "monitor api status", ["key_api"],
                                                                          result)), mimetype="text/plain")


if __name__ == '__main__':
    # fetch config
    with open("./config.yaml", 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    result = {}
    # phase2 = {}

    # Start up the server to expose the metrics.
    port = config["global"]["port"]

    app.run(host="0.0.0.0", port=port)
