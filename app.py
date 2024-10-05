from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="34.69.45.129",
            user="easy_user",
            password="agxXU{A}m'0uGd)~",
            database="easy_crop_app_db"
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

@app.route('/add_location', methods=['POST'])
def add_location():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract latitude and longitude
        loc_lat = data['latitude']
        loc_long = data['longitude']

        # Extract weather data
        weather = data['weather']
        loc_max_temp = weather['maxTemperature']
        loc_min_temp = weather['minTemperature']
        loc_wind_speed = weather['windSpeed']
        loc_wind_degree = weather['windDirection']
        loc_pression = weather['pressure']
        
        # Extract precipitation values
        precip_1h = weather['precip1h']
        precip_24h = weather['precip24h']

        # Extract and convert sunrise and sunset times to datetime
        sunrise = datetime.fromisoformat(weather['sunrise'].replace("Z", "+00:00"))  # Convert to datetime
        sunset = datetime.fromisoformat(weather['sunset'].replace("Z", "+00:00"))    # Convert to datetime

        # Create a database connection
        connection = create_connection()
        cursor = connection.cursor()

        # Prepare and execute the SQL insert statement
        query = """
            INSERT INTO weather_data (latitude, longitude, wind_direction, temperature_2m, max_temperature_24h, min_temperature_24h, pressure_msl, precipitation_1h, precipitation_24h, sunrise, sunset)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            loc_lat,                     # latitude
            loc_long,                    # longitude
            loc_wind_degree,             # wind_direction
            weather['temperature'],       # temperature_2m
            loc_max_temp,                # max_temperature_24h
            loc_min_temp,                # min_temperature_24h
            loc_pression,                # pressure_msl
            precip_1h,                   # precipitation_1h
            precip_24h,                  # precipitation_24h
            sunrise,                     # sunrise (datetime object)
            sunset                       # sunset (datetime object)
        )

        cursor.execute(query, values)
        connection.commit()

        return jsonify({"message": "Weather data added successfully!"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)

