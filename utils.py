import requests
import os
import random
from datetime import datetime


def generate_photo(photo_reference, place_id):
    payload = {
        "key": os.getenv("GOOGLE_API_KEY"),
        "maxwidth": 700,
        "photoreference": photo_reference,
    }
    response = requests.get(
        url="https://maps.googleapis.com/maps/api/place/photo", params=payload
    )
    if response.status_code == 200:
        # Extract the photo data from the response
        photo_data = response.content

        # Save the photo data to a file
        with open(f"media/{place_id}.jpg", "wb") as f:
            f.write(photo_data)
        return True
    return False


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


def constuct_location_link(lng, lat):
    link = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    return link
