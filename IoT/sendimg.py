from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the image file on the Raspberry Pi
IMAGE_FILE_PATH = '/home/pi/Documents/test.jpg'

@app.route('/image')
def get_image():
    try:
        return send_file(IMAGE_FILE_PATH, mimetype='image/jpg')
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)