from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from coordinates import get_gps_data

import Adafruit_DHT

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Replace 'port' with your React.js project's port
socketio = SocketIO(app, cors_allowed_origins="*")

# Define GPIO pin for DHT11 sensor
#DHT_SENSOR = Adafruit_DHT.DHT11
#DHT_PIN = 4

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
"""
def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        data = {
            'temperature': temperature,
            'humidity': humidity
        }
        return data
    else:
        return {'error': 'Failed to read sensor data'}
"""
@socketio.event
def read_sensor_data():
    while True:
        lat, long = get_gps_data()
        data = {
            'lat': lat,
            'long': long
        }
        socketio.emit('gps', {'data':data})
        socketio.sleep(2)
    
        
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

