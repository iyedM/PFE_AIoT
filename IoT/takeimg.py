from picamera2 import Picamera2, Preview
import time

def capture_image():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (800, 600)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    #picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("/home/pi/Desktop/test.jpg")
    picam2.close()
    return "/home/pi/Desktop/test.jpg"
# Call the function
image_path = capture_image()

# Display the path of the captured image
print("Image captured and saved at:", image_path)
