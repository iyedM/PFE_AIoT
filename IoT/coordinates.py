import gpsd

gpsd.connect()

def get_gps_data():
    packet = gpsd.get_current()
    return packet.lat, packet.lon
lat, lon = get_gps_data()
print("Latitude:",lat , "Longitude", lon)
