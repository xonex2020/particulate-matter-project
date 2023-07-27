

# Particulate matter Project

### Features
- Support Raspberry Pi (recommended)
- Possible practical implementation of the measuring station 
- Different variations of implementation for experienced and non-experienced users
- Easy deployment via Docker / Docker-Compose
- Dashboard to monitor the values
- Obtaining relevant system information of the measuring station and platform 



<!--
Clone Project
--> 

## first download the project

clone the project:

    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt install git nano curl -y

    git clone https://github.com/xonex2020/particulate-matter-project.git

    cd particulate-matter-project
    

update the project:

    git pull
<!--
Install requirements
--> 

# install requirements:

- python3, python3-pip
- docker
- docker-compose


## easy install script

easy-install:
    
    chmod +x install-requirements.sh
    ./install-requirements.sh

## manual install

install requirements(download the requirements.txt for the pip depdependencies):

    sudo apt install python3 python3-pip -y
    sudo pip install -r requirements.txt

    
install docker:

    curl -sSL https://get.docker.com/ | CHANNEL=stable sh

Nachdem der Installationsprozess abgeschlossen ist, müssen Sie eventuell den Dienst aktivieren und sicherstellen, dass er gestartet ist (z. B. CentOS 7)

    systemctl enable --now docker



install docker compose (Standalone - version):

    LATEST=$(curl -Ls -w %{url_effective} -o /dev/null https://github.com/docker/compose/releases/latest) && LATEST=${LATEST##*/} && curl -L https://github.com/docker/compose/releases/download/$LATEST/docker-compose-$(uname -s)-$(uname -m) > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose





# Install InfluxDB & Grafana (Docker-Compose)

For these commands you must be in the project folder.

run & pull the container:
    
    docker compose up -d


stop the container:

    docker compose down


restart the container:

    docker compose restart


for update the container(pull new image and recreate the container):

    docker compose pull
    docker compose up -d



### create your first bucket for your sensor measurements

How is my ip from the device?

    ip a

lets login to InfluxDB
    
    http://my-pi-ip:8086



####Get Started with InfluxDB
                
1. Setup Initial User (Remember your organization name and your bucket name for later)
2. Copy your API Token for later
3. Click on Quick Start



## lets make the Sensor ready:


edit the .env and set the required data. -> 
    
    sudo nano .env

In some cases you have another serial port. You can identify the serial port with this command:

    dmesg | grep ttyUSB

in my case 

    /dev/ttyUSB0


## The script for the Sensor: (not recommended -> please use the sensor.py from the git clone!)  

```python
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

```


<!--
Start measurement
-->
# Start the measurement with Cron

Lets create a new crontab
    
    crontab -e

abbend a new crontab for example fair every 15 minutes:
    
    */15 * * * * /usr/bin/python3 /DESTINATION FROM THE SENSOR.PY FILE

For a custom time setting use the [Cron Guru :)](https://crontab.guru/ "link title")
with it you can easily set your individual time.



## Setup Grafana

Login to Grafana

    http://my-pi-ip:3000


Placeholder Example Dashboard