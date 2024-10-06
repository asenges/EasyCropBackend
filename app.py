from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

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

@app.route('/weather_growth_analytic', methods=['POST'])
def add_weather_growth_analytic():
    try:
        data = request.get_json()
        loc_lat = data['latitude']
        loc_long = data['longitude']
        weather = data['weather']
        loc_wind_degree = weather['windDirection']
        loc_temperature_2m = weather['temperature_2m']
        loc_max_temp = weather['maxTemperature']
        loc_min_temp = weather['minTemperature']
        loc_pressure = weather['pressure']
        precip_1h = weather['precip1h']
        precip_24h = weather['precip24h']
        sunrise = datetime.fromisoformat(weather['sunrise'].replace("Z", "+00:00"))
        sunset = datetime.fromisoformat(weather['sunset'].replace("Z", "+00:00"))
        request_date = datetime.now()
        prediction_date = datetime.fromisoformat(data.get('prediction_date').replace("Z", "+00:00")) if data.get('prediction_date') else None
        plant_id = data.get('plant_id')
        km_radius = data.get('km_radius')
        sow_date = datetime.fromisoformat(data.get('sow_date').replace("Z", "+00:00")) if data.get('sow_date') else None

        connection = create_connection()
        cursor = connection.cursor()

        query_growth_analytic = """
            INSERT INTO weather_growth_analytic (
                latitude, longitude, wind_direction, temperature_2m, max_temperature_24h, 
                min_temperature_24h, pressure_msl, precipitation_1h, precipitation_24h, 
                sunrise, sunset, request_date, prediction_date, plant_id, km_radius, sow_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values_growth_analytic = (
            loc_lat,
            loc_long,
            loc_wind_degree,
            loc_temperature_2m,
            loc_max_temp,
            loc_min_temp,
            loc_pressure,
            precip_1h,
            precip_24h,
            sunrise,
            sunset,
            request_date,
            prediction_date,
            plant_id,
            km_radius,
            sow_date
        )

        cursor.execute(query_growth_analytic, values_growth_analytic)
        connection.commit()

        return jsonify({"message": "Weather growth analytics data added successfully!"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/weather_growth_analytic_by_id', methods=['GET'])
def get_weather_growth_analytic_by_id():
    # Get the id from query parameters
    id = request.args.get('id', type=int)

    if id is None:
        return jsonify({"error": "ID parameter is required."}), 400

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Modify the query to include a JOIN with the plants_data table
        query = """
            SELECT 
            weather_growth_analytic.id AS weather_analytic_id, 
            weather_growth_analytic.*,
            plants_data.id AS plant_id, 
            plants_data.*
            FROM weather_growth_analytic
            LEFT JOIN plants_data ON plants_data.id = weather_growth_analytic.plant_id
            WHERE weather_growth_analytic.id = %s
        """
        
        cursor.execute(query, (id,))
        row = cursor.fetchone()  # Use fetchone since we're looking for a single item
        
        if not row:
            return jsonify({"message": "No data found for the specified ID."}), 404

        return jsonify(row), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# Endpoint to get weather growth analytics data
@app.route('/weather_growth_analytic', methods=['GET'])
def get_weather_growth_analytic():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM weather_growth_analytic"
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Endpoint to get plant data
@app.route('/plants_data', methods=['GET'])  # Updated endpoint
def get_plant_data():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM plants_data"  # Query from plants_data
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Endpoint to handle historical weather data (GET)
@app.route('/historic_weather_data', methods=['GET'])
def get_historic_weather_data():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM historic_weather_data"  # Adjust this to your actual table name
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify(rows), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Endpoint to add weather predictions data
@app.route('/weather_predictions', methods=['POST'])
def add_weather_prediction():
    try:
        data = request.get_json()
        # Assume you have similar fields as in weather_growth_analytic, adjust accordingly
        weather_growth_analytic_id = data.get('weather_growth_analytic_id')
        predicted_month = data.get('predicted_month')
        predicted_year = data.get('predicted_year')
        predicted_wind_speed_10m = data.get('predicted_wind_speed_10m')
        predicted_wind_dir_10m = data.get('predicted_wind_dir_10m')
        predicted_t_2m = data.get('predicted_t_2m')
        predicted_t_max_2m_24h = data.get('predicted_t_max_2m_24h')
        predicted_t_min_2m_24h = data.get('predicted_t_min_2m_24h')
        predicted_msl_pressure = data.get('predicted_msl_pressure')
        predicted_precip_1h = data.get('predicted_precip_1h')
        predicted_precip_24h = data.get('predicted_precip_24h')
        prediction_date = datetime.now()
        accuracy = data.get('accuracy')
        success_rate = data.get('success_rate')
        user_input = data.get('user_input')
        environmental_impact = data.get('environmental_impact')
        user_feedback = data.get('user_feedback')
        result_precision = data.get('result_precision')
        recall = data.get('recall')

        connection = create_connection()
        cursor = connection.cursor()

        query_prediction = """
            INSERT INTO weather_predictions (weather_growth_analytic_id, predicted_month, predicted_year, predicted_wind_speed_10m, predicted_wind_dir_10m, predicted_t_2m, predicted_t_max_2m_24h, predicted_t_min_2m_24h, predicted_msl_pressure, predicted_precip_1h, predicted_precip_24h, prediction_date, accuracy, success_rate, user_input, environmental_impact, user_feedback, result_precision, recall)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values_prediction = (
            weather_growth_analytic_id,
            predicted_month,
            predicted_year,
            predicted_wind_speed_10m,
            predicted_wind_dir_10m,
            predicted_t_2m,
            predicted_t_max_2m_24h,
            predicted_t_min_2m_24h,
            predicted_msl_pressure,
            predicted_precip_1h,
            predicted_precip_24h,
            prediction_date,
            accuracy,
            success_rate,
            user_input,
            environmental_impact,
            user_feedback,
            result_precision,
            recall
        )

        cursor.execute(query_prediction, values_prediction)
        connection.commit()

        return jsonify({"message": "Weather prediction data added successfully!"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Endpoint to get weather predictions data
@app.route('/weather_predictions', methods=['GET'])
def get_weather_predictions():
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM weather_predictions"  # Query from weather_predictions
        cursor.execute(query)
        rows = cursor.fetchall()
        return jsonify(rows), 200

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
