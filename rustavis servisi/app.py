import os
from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
import requests

app = Flask(__name__, static_folder='static')

# Google Maps API Key (replace with your own)
google_maps_api_key = "AIzaSyDsE3PSJh4qlvp7u6ctGLGPjt-y2MN1W2I"

# Initialize geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

@app.route('/')
def index():
    return render_template('index.html', api_key=google_maps_api_key)

@app.route('/get_location')
def get_location():
    ip_address = request.remote_addr
    url = f"http://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    data = response.json()
    location = data.get("loc", "").split(",")
    if len(location) == 2:
        latitude, longitude = location
        return jsonify({"latitude": latitude, "longitude": longitude})
    return jsonify({"error": "Unable to fetch location"})

@app.route('/directions', methods=['POST'])
def directions():
    origin = request.form.get('origin')
    destination = request.form.get('destination')
    directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={google_maps_api_key}"
    response = requests.get(directions_url)
    directions_data = response.json()

    if "routes" in directions_data and directions_data["routes"]:
        # Check if routes exist and are not empty
        return render_template('directions.html', data=directions_data)
    else:
        error_message = "Unable to retrieve directions."
        return render_template('directions.html', error=error_message)

@app.route('/home')
def home():
    return render_template('index.html', api_key=google_maps_api_key)



if __name__ == '__main__':
    app.run(debug=True)
