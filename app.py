from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()
print(os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)


@app.route("/nearby-places", methods=["GET"])
def get_nearby_places():
    """
    Send a request to google places api to get the nearby places of intrest to the user

    """

    API_KEY = os.getenv("GOOGLE_API_KEY")
    URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    payload = {
        "key": API_KEY,
        "location": f"{request.args.get('lng')}, {request.args.get('lat')}",
        "radius": "1000",
        "keyword": request.args.get("type"),
    }
    results = requests.get(URL, params=payload)
    if results.status_code == 200:
        response = []
        places_data = results.json()
        for place in places_data["results"]:
            response_dict = {}
            response_dict["name"] = place["name"]
            response_dict["location"] = place["geometry"]["location"]
            response.append(response_dict)
    return jsonify(response)
