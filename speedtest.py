import re
import subprocess
from csv import writer
import datetime
import config
from influxdb import InfluxDBClient


speed_test_response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple',
                                       shell=True,
                                       stdout=subprocess.PIPE).stdout.read().decode('utf-8')


ping = re.findall('Ping:\s(.*?)\s', speed_test_response, re.MULTILINE)[0]
download = re.findall('Download:\s(.*?)\s', speed_test_response, re.MULTILINE)[0]
upload = re.findall('Upload:\s(.*?)\s', speed_test_response, re.MULTILINE)[0]


now = str(datetime.datetime.now()).split(' ')
date_now = now[0]
time_now = now[1]


def append_values_in_csv(file_name):
    values = [date_now, time_now, ping, download, upload]
    with open(file_name, 'a') as write_object:
        csv_writer = writer(write_object)
        csv_writer.writerow(values)


def append_values_to_influxdb():
    speed_data = [
        {
            "measurement": "internet_speed",
            "tags": {
                "host": 'homeserver'
            },
            "fields": {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }
    ]

    client = InfluxDBClient(config.ip,
                            config.port,
                            config.user,
                            config.password,
                            config.speed_test_database)

    client.write_points(speed_data)


append_values_to_influxdb()

