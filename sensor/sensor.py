
import time, schedule, serial, influxdb_client, os
from dotenv import find_dotenv, load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv(find_dotenv())

# InfluxDB Connection informationen
influxdb_token = os.getenv("influxdb_token")
org = os.getenv("influxdb_organisation")
bucket = os.getenv("influxdb_bucket")
influx_url= os.getenv("influxdb_url")
client = InfluxDBClient(url=influx_url, token=influxdb_token)

#serial_port
serial_port= os.getenv("serial_port")

# Aufbau der serial connection  mit einer baurate von 9600
ser = serial.Serial(serial_port, baudrate=9600, stopbits=1, parity="N", timeout=2)

def job():
    time.sleep(1)
    s = ser.read(1)
    if ord(s) == int("AA", 16):
        s = ser.read(1)
        if ord(s) == int("C0", 16):
            s = ser.read(7)
            a = []
            for i in s:
                a.append(i)
            pm2highbyte = s[0]
            pm2lowbyte = s[1]
            pm10highbyte = s[2]
            pm10lowbyte = s[3]

            # Speichern der Sensordaten in result pm25,10
            resultPm25 = float(pm2highbyte + pm2lowbyte * 256) / 10.0
            resultPm10 = float(pm10highbyte + pm10lowbyte * 256) / 10.0

            print("PM2.5 - ", float(pm2highbyte + pm2lowbyte*256)/10.0 ," PM10 - ", float(pm10highbyte + pm10lowbyte*256)/10.0)
            time.sleep(1)
            # Schreiben der Daten in die InfluxDB
            write_api = client.write_api(write_options=SYNCHRONOUS)

            p = influxdb_client.Point("Feinstaub") \
                .tag("sensor", "sensor1") \
                .field("pm25", resultPm25) \
                .field("pm10", resultPm10)
            write_api.write(bucket=bucket, org=org, record=p)

# Zeitintervall default 15min
schedule.every(15).minutes.do(job)

def main():
    job()

if __name__ == "__main__":
    main()