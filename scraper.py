import requests
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup

import site_parsing

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/feed', methods=['POST'])
@cross_origin()
def get_feed():
    ''' Accepts a JSON in the format:
        {
            'sites': [
                "reddit",
                "cbc",
                "ctv"
            ],
            
            'keywords': [
                "canada"
            ],
            'urgency': alert
        }

        Returns a JSON:
        {
            "feed": [
                {
                    "title": ...,
                    "url": ...,
                    "summarized_body": ...,
                }
            ]
        }
    '''

    # Get request
    req_body = request.get_json()

    # Initialize to-return JSON
    results = {"feed": []}
    print results
    # Begin scraping
    for site in req_body["sites"]:
        sub_feed = site_parsing.get_site_feed(site, req_body["keywords"], req_body["urgency"])
        results["feed"].extend(sub_feed)
    results["feed"] = sorted(results["feed"], key=lambda x: x["time"], reverse = True)
    return jsonify(results)

if __name__== '__main__':
    app.run(host='0.0.0.0')
