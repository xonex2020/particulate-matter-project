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


<!--
Install requirements
-->

## install requirements:

- Python3
- Python - pip
- curl, git
- requirements via requirements.txt

install requirements:

    sudo apt update && sudo apt upgrade -y

    sudo apt install python3 python3-pip curl git -y

    



## install Docker:





    curl -sSL https://get.docker.com/ | CHANNEL=stable sh



Nachdem der Installationsprozess abgeschlossen ist, müssen Sie eventuell den Dienst aktivieren und sicherstellen, dass er gestartet ist (z. B. CentOS 7)

    systemctl enable --now docker



## install docker compose:


(Standalone - version)

    LATEST=$(curl -Ls -w %{url_effective} -o /dev/null https://github.com/docker/compose/releases/latest) && LATEST=${LATEST##*/} && curl -L https://github.com/docker/compose/releases/download/$LATEST/docker-compose-$(uname -s)-$(uname -m) > /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose



<!--
Install InfluxDB  docker run
-->


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




## simplest structure
  ### Content for the simplest structure
  - Script for the sensor
  - Automatic continuous measurement



Python script

    python script


cronjob

    python script


Um die Zeit anzupassen empfiehlt es sich einen calculator zu verwenden der die arbeit erleichtert. [Crontab Guru :)](https://crontab.guru/ "link title")
