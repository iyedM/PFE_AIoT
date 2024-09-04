import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

def predict_wheat_class(image_path):
    image = Image.open(image_path)
    IMAGE_SIZE = (100, 100)
    image = image.resize(IMAGE_SIZE)
    image = np.array(image, dtype=np.float32) / 255.0
    image = np.expand_dims(image, axis=0)

    interpreter = tflite.Interpreter(model_path='/home/pi/Documents/fp_16_model.tflite')
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class_index = np.argmax(output_data[0])

    if output_data.squeeze() < 0.5:
        predicted_class_name = "damaged wheat"
    else:
        predicted_class_name = "good wheat"

    return predicted_class_name

# Call the function with the image path
image_path = "/home/pi/Desktop/wheat1.jpg"  # Replace with the actual path to your image
predicted_class = predict_wheat_class(image_path)

# Display the predicted class
print("this wheat is a :", predicted_class)
