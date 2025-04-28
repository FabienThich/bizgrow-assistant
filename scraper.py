from dotenv import load_dotenv
from flask import Flask, jsonify
import json
import os

load_dotenv()

import googlemaps # type: ignore

API_KEY = os.getenv("GOOGLE_API_KEY")
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

display_data = {}

places = gmaps.places(
    query="Bubble Tea",
    radius=0.5,
    location=(os.getenv("LOCATION_CORDS")),
    region="CA",
)

for index, place in enumerate(places["results"]):
    if index == 3:
        break
    # print(index, place)

    print(f"Name: {place['name']}")
    print(f"place_id: {place['place_id']}")
    print(f"Address: {place['formatted_address']}")

    if "photos" in place:
        for photo in place["photos"]:
            if "html_attributions" in photo:
                print(f"Photo: {photo['html_attributions']}")

            else:
                print("No photo available")

    display_data[place["name"]] = {
        "place_id": place["place_id"],
        "address": place["formatted_address"],
    }

    print("-" * 40)


# get details of the place (gives all the attributes of the place)
# print(places['results'])

# print(len(places['results']))


place = gmaps.place(
    place_id=os.getenv("PLACE_ID"),
    fields=["name", "vicinity", "rating", "formatted_phone_number", "review"],
)

print(place["result"]["name"])
print(place["result"]["vicinity"])
print(place["result"]["rating"])
print(place["result"]["formatted_phone_number"])
# print(place["result"]["reviews"])


@app.route("/places", methods=["GET"])
def get_places():
    return jsonify(place['result']['reviews'])


@app.route("/")
def home():
    return "Hello world bro!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
