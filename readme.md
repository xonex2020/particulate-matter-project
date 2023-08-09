

# Particulate matter Project

### Features
- Support Raspberry Pi 64 Bit (recommended)
- On Raspberry Pi you have to use the 64 Bit Version!
- Possible practical implementation of the measuring station 
- Different variations of implementation for experienced and non-experienced users
- Easy deployment via Docker
- Dashboard to monitor the values


<!--
Clone Project
--> 

## Clone the Project from GitHub

clone the project:

    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt install git nano curl -y

    git clone https://github.com/xonex2020/particulate-matter-project.git

    cd particulate-matter-project
    

When you wand update the project use:

    git pull
<!--
Install requirements
--> 

# Install requirements via install script or manual:

- python3, python3-pip + requirements
- docker

### install script

easy-install:
    
    chmod +x install-requirements.sh
    ./install-requirements.sh

Please reboot your Device
### manual install

install requirements(download the requirements.txt for the pip depdependencies):

    sudo apt install libffi-dev libssl-dev python3-dev python3 python3-pip -y
    
install docker:

    curl -sSL https://get.docker.com/ | CHANNEL=stable sh

    sudo usermod -aG docker ${USER}

    systemctl enable --now docker

    sudo reboot




# Setup InfluxDB

Here you can edit the variables (PASSWORD,USERRNAME,ORG,BUCKET) note it for later you will need them in Grafana.

    docker run -d -p 8086:8086 \
      -v $PWD/data:/var/lib/influxdb2 \
      -v $PWD/config:/etc/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=testuser \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=testpw123. \
      -e DOCKER_INFLUXDB_INIT_ORG=TestOrg \
      -e DOCKER_INFLUXDB_INIT_BUCKET=test_bucket \
      influxdb:latest



login to InfluxDB

    http://my-pi-ip:8086


When you don't know your own ip use ip a.
    
    ip a


### Now we have to create a token:

1. Login to InfluxDB
2. Go in the left Menubar on API Tokens
3. Click on Generate API Token -> All Access Token
4. Set a Name for your Token like Grafana and save it
5. Important copy your token for later! 

#### We have step-by-step pictures on GitHub for all steps



## Now we have to setup the sensor:

You can use the default sensor script in he cloned project folder or create it on your own.

### edit the .env and set the required data. 
    
    cd sensor
    sudo nano .env

here we change the url and api token

    influxdb_token= your token
    influxdb_organisation= your org
    influxdb_bucket= your bucket
    influxdb_url= http://my-pi-ip:8086
    serial_port=/dev/ttyUSB0

In some cases you have another serial port. You can identify the serial port with this command:

    dmesg | grep ttyUSB

in my case 

    /dev/ttyUSB0


### The sensor.py script for all that want create it on there own:

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
# schedule.every(15).minutes.do(job)

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
install Grafana via Docker

    docker run -d -p 3000:3000 --name=grafana \
    --volume grafana-storage:/var/lib/grafana \
    grafana/grafana

Login to Grafana (on first install it can take a while until you see the login screen)

    http://my-pi-ip:3000

Login data for the first login
    
    username: admin
    password: admin

now you have to set your own password.

### Import the Dashboard Template from the json file:

1. In the left menu click on Dashboard
2. On the right side select New -> Import
3. Upload dashboard JSON file -> Load (The Template is here on GitHub)
4. Now we have to add the DataSource right menu -> Connections -> Data sources
5. select InfluxDB
6. Set the Query Language to Flux
7. disable under Auth -> Basic auth
8. Add your InfluxDB token and the Organisation under InfluxDB Details and click on Save & test
9. Switch to your Dashboard and click in the right conor from your graphs on edit 
10. here you have to click one time in the query for influxDB and click on Save -> Apply
11. This Part repeat for all your graphs in the Dashboard.

    
#### We have step-by-step pictures on GitHub for all steps

