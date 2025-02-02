import requests
import json
from flask import Flask, request, render_template, session, url_for, jsonify
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("APP_SECRET", "4TM2NBktihlGzCTRQqLAYooSs3QD_h_fLGmoq2sROj4sNgV8i7KROHxu4RdNsbFUy3k")
app.config['SESSION_COOKIE_SECURE'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

url = "https://seal-app-aafp5.ondigitalocean.app/query"
headers = {
    'Authorization': 'Bearer ' + os.environ.get("BEARER_TOKEN"),
    'Content-Type': 'application/json'
}

# csrf = CSRFProtect(app)

@app.route("/")
# @csrf.exempt
def home():
    return render_template("index.html")

@app.post("/searchResult")
def searchResult():
    query = request.form['query']

    payload = json.dumps({
    "queries": [
        {
            "query": query
        }
    ]
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    
    data = json.loads(response.text)
    try:
        if len(data["results"][0]["results"]) and  data["results"][0]["results"][0]["score"] > .2:
            context = {
                "query": query,
                "results":data["results"][0]["results"]
            }
        else:
            context = {
                "query": query,
                "results":{"results":[
                {
                "results":[
                    {
                        "text": "Sorry, I don't have answer for this query. Kindly contact your HR or call EPFO Helpline for more information 1800118005.", 
                        "score":1.0
                    }
                ]
                }
                ]
                }
            }
    except:
            context = {
                 "query": query,
                    "results":{"results":[
                    {
                        "results":[
                            {
                                "text": "Sorry, I don't have answer for this query. Kindly contact your HR or call EPFO Helpline for more information 1800118005.", 
                                "score":1.0
                            }
                        ]
                    }
                    ]
                }
            }


    return render_template("search_results.html", context=context)
