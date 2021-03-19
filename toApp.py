import requests
import json
import glob
import time
import board
import busio
import adafruit_veml7700
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#setting up temp sensor
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#setting up moisture/light sensor
i2c = busio.I2C(board.SCL, board.SDA)
veml7700 = adafruit_veml7700.VEML7700(i2c)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def getLux():
        return veml7700.lux
def getMoisture():
    return chan.value

#formatting string
temp_f = format( read_temp()[1], ".1f")
lux = format( getLux(), ".1f")
moisture = format( getMoisture(), ".1f")

url = "https://dmrgrt9jnf.execute-api.us-east-2.amazonaws.com/dev/addData"

payload = json.dumps({
  "AccessToken": " ",
  "Data": {
    "plantType": "insert scientific name here",
    "potId": "230",
    "potName": "NewTest",
    "photosensor": lux,
    "reservoirLevel": "64",
    "soilMoisture": moisture,
    "temp": temp_f
  }
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


