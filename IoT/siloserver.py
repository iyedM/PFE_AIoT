from flask import Flask, render_template, jsonify, send_file,Response
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet
import random
from dht11 import read_dht11_data
from takeimg import capture_image
from modelrun import predict_wheat_class
#from coordinates import get_gps_data
#from poids import measure_weight

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})
# Allow requests from localhost:3000
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

thread_running = False

def upload_data():
    humidity, temperature = read_dht11_data()
    return {"humidity":humidity, "temperature":temperature}
def background_thread():
    global thread_running
    while thread_running:
        environment_data = upload_data()
        socketio.emit('random_location', {'data': environment_data})
        socketio.sleep(1)  # Sends a message every 8 seconds

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
#image_path="/home/pi/Desktop/test.jpg"
@app.route('/data')
def get_data():
    #humidity, temperature = read_dht11_data()
    #lat, long = get_gps_data()
    #weight = measure_weight()
    weight = 140
    return jsonify(weight = weight)

@app.route('/image')
def get_image():
    image_path=capture_image()

#    image_path ="/home/pi/Desktop/test.jpg"

    # Open the image file
    with open(image_path, "rb") as f:
        image_data = f.read()


    # Return a Response object with image data and custom headers
    return Response(image_data)
@app.route('/quality')
def get_quality():
    result = predict_wheat_class(image_path)
    return jsonify(result = result)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
