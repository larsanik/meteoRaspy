# Get and send meteo data from bmp180 and ant10 to server.
from ant10 import AHT10
from bmp180_a import readBmp180
import requests
import json
from datetime import datetime


def getMeteoData():
    m = AHT10(1)
    data = m.getData()
    temperature_aht10 = data[0]
    humidity_aht10 = data[1]
    temperature_bmp180, pressure_bmp180, altitude_bmp180 = readBmp180()
    pressure_bmp180_mmhg = pressure_bmp180 / (100.0 * 1.333)
    return temperature_aht10, humidity_aht10, temperature_bmp180, pressure_bmp180_mmhg


def sendMeteoData(temperature_in, humidity_in, pressure_in):
    # target URL
    url = 'http://larsanik.sknt.ru/meteodata/post_q/'

    # data in dictionary
    idstation = 1
    timemes = str(datetime.today())
    temperature = temperature_in
    humidity = humidity_in
    press = pressure_in
    geocoord = '38.161594892513094, 20.43207143133511'

    param = {
        'ID station': idstation,
        'Date&time measurement': timemes,
        'Temperature': temperature,
        'Humidity': humidity,
        'Pressure': press,
        'Geocoord': geocoord
    }
    # print(f'Словарь = {param}')

    # encode the dictionary into the format JSON
    json_param = json.dumps(param)

    # sending a POST request with data in the format JSON
    resp = requests.post(url, data=json_param)
    # print(f'Server response = {resp}')


# call
if __name__ == '__main__':
    # get data
    temperature_aht10, humidity_aht10, temperature_bmp180, pressure_bmp180_mmhg = getMeteoData()
    # send data
    sendMeteoData(temperature_aht10, humidity_aht10, pressure_bmp180_mmhg)


