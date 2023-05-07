from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os
import random
from datetime import datetime

load_dotenv()

app = Flask(__name__)


def get_random_item(mylist):
    return random.choice(mylist)


def calculate_time_delta(from_time, to_time, activities_no):
    from_time_obj = datetime.strptime(from_time, "%H:%M:%S").time()
    to_time_obj = datetime.strptime(to_time, "%H:%M:%S").time()
    delta = datetime.combine(datetime.min, to_time_obj) - datetime.combine(
        datetime.min, from_time_obj
    )
    time_diff = delta / activities_no
    return str(time_diff)


@app.route("/nearby-places", methods=["GET"])
def get_nearby_places():
    """
    Send a request to google places api to get the nearby places of intrest to the user
    """

    API_KEY = os.getenv("GOOGLE_API_KEY")
    URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    places_types = request.args.get("types").split("|")
    from_time = request.args.get("from_time")
    to_time = request.args.get("to_time")
    response = []

    for place_type in places_types:
        response_dict = {}
        payload = {
            "key": API_KEY,
            "location": f"{request.args.get('lng')}, {request.args.get('lat')}",
            "radius": "1000",
            "type": place_type,
        }
        results = requests.get(URL, params=payload)
        if results.status_code == 200:
            places_data = results.json()["results"]
            random_place = get_random_item(places_data)

            simple_place_data = {
                "name": random_place["name"],
                "location": random_place["geometry"]["location"],
                "types": random_place["types"],
                "activity_duration": calculate_time_delta(
                    from_time, to_time, len(places_types)
                ),
            }
            response_dict[place_type] = simple_place_data
            response.append(response_dict)
    return jsonify(response)
