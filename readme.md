### Features
- Support Raspberry Pi (recommended)
- Possible practical implementation of the measuring station 
- Different variations of implementation for experienced and non-experienced users
- Easy deployment via Docker / Docker-Compose
- Dashboard to monitor the values
- Obtaining relevant system information of the measuring station and platform 


# Particulate matter Project



<Placeholder Icons (stars/forks/tag/release/issues)


**Table of Contents**

## InfluxDB

Run InfluxDB via docker run: (edit you data pw,username..)

    docker run -d --restart -p 8086:8086 \
      -v $PWD/data:/var/lib/influxdb2 \
      -v $PWD/config:/etc/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=myuser \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=mypw123. \
      -e DOCKER_INFLUXDB_INIT_ORG=my_org\
      -e DOCKER_INFLUXDB_INIT_BUCKET=my_bucket \
      influxdb:2.0


## install Docker

[Install docker on Raspberry Pi](https://docs.docker.com/engine/install/raspbian/) for other unix plattforms check the install docs.



## simplest structure
  ### Content for the simplest structure
  - Docker
  - InfluxDB
  - Script for the sensor
  - Automatic continuous measurement

[For Docker install click here](https://docs.docker.com/engine/install/raspbian/ "link title")
