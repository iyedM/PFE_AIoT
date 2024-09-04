# weight_measurement.py

from hx711 import HX711
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

def measure_weight():
    try:
        hx711 = HX711(
            dout_pin=5,    # Output
            pd_sck_pin=6,  # Input clock to the HX711
            channel='A',
            gain=128       # It may be 32, 64, 128
        )
        hx711.reset()
        print("after reset")
        # Collect multiple raw data readings
        num_readings = 10  # Adjust this value as needed
        measures = []
        for _ in range(num_readings):
            measures.append(hx711.get_raw_data())

        # Flatten the list of lists
        flat_measures = [item for sublist in measures for item in sublist]

        # Calculate the average of the readings
        avg_measure = sum(flat_measures) / (num_readings * len(measures[0]))  # Dividing by total number of readings

        # Apply calibration factor
        calibration_factor = 200 / 712841.93
        calibrated_weight = avg_measure * calibration_factor

        return calibrated_weight

    finally:
        GPIO.cleanup()  # Always do a GPIO cleanup in your scripts!
weight = measure_weight()

# Now you can use the `weight` variable as needed
print("Measured weight:", weight, "grams")