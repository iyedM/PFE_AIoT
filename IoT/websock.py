#Transporter Server
from flask import Flask
from flask_socketio import SocketIO
import eventlet
import random
from dht11 import read_dht11_data
from coordinates import get_gps_data
#from poids import measure_weight

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Coordinates for the bounding box of Tunisia
TUNISIA_BOUNDS = {
    "min_lat": 30.0,
    "max_lat": 37.5,
    "min_lon": 7.5,
    "max_lon": 11.5
}
global temperature
global humidity
global lat
global long
lat, long = get_gps_data()
humidity, temperature = read_dht11_data()

# Control variable for the background thread
thread_running = False

def upload_data():
    humidity, temperature = read_dht11_data()
    #weight = measure_weight()
    weight = 150
    lat, long = get_gps_data()
    #global lat
    #lat= lat+0.02
    #global long
    #long= long+0.02
    return {"lat": lat, "lon": long, "humidity":humidity, "temperature":temperature,"weight": weight}

def background_thread():
    global thread_running
    while thread_running:
        transportation_data = upload_data()
        socketio.emit('random_location', {'data': transportation_data})
        socketio.sleep(8)  # Sends a message every 8 seconds

@socketio.on('connect')
def handle_connect():
    global thread_running
    print('Client connected')
    thread_running = True
    socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def handle_disconnect():
    global thread_running
    print('Client disconnected')
    thread_running = False

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
