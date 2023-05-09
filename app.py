from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import requests
import os

from .utils import (
    generate_photo,
    get_random_item,
    calculate_time_delta,
    constuct_location_link,
)

UPLOAD_FOLDER = "media\\"
ALLOWED_EXTENTIONS = set(["jpg", "png", "jpeg"])

load_dotenv()

app = Flask(__name__)
app.debug = True
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/media/uploads/<filename>")
def uploaded_file(filename):
    """Expose media files through out urls"""

    return send_file(app.config["UPLOAD_FOLDER"] + filename, mimetype="image/jpeg")


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
        simple_place_data = {}
        payload = {
            "key": API_KEY,
            "location": f"{request.args.get('lat')}, {request.args.get('lng')}",
            "radius": "3000",
            "type": place_type,
        }
        results = requests.get(URL, params=payload)
        if results.json()["status"] == "ZERO_RESULTS":
            return jsonify({"error": "No results found!"}), 404
        print(payload)
        if results.status_code == 200:
            places_data = results.json()["results"]
            random_place = get_random_item(places_data)
            photo_url = None
            if "photos" in random_place.keys():
                photo_ref = random_place["photos"][0]["photo_reference"]
                if generate_photo(photo_ref, random_place["place_id"]):
                    photo_url = f"http://localhost:5000/media/uploads/{random_place['place_id']}.jpg"

            lat = random_place["geometry"]["location"]["lat"]
            lng = random_place["geometry"]["location"]["lng"]
            simple_place_data = {
                "activity_type": place_type,
                "name": random_place["name"],
                "location": constuct_location_link(lng, lat),
                "types": random_place["types"],
                "activity_duration": calculate_time_delta(
                    from_time, to_time, len(places_types)
                ),
                "photo": photo_url,
            }

            response.append(simple_place_data)
    return jsonify(response)
