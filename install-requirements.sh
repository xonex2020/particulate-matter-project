#!   /bin/bash -e

RED='\033[0;31m'  
NOCOLOR='\033[0m'


# Install Requirements
echo -e "${RED}install dependencies and requirements"
echo -e "${NOCOLOR} lets go"
sudo apt update && sudo apt upgrade -y && sudo apt install libffi-dev libssl-dev python3-dev python3 python3-pip -y
sudo pip3 install docker-compose schedule pyserial influxdb-client python-dotenv

# Install docker
echo -e "${RED}install docker"
echo -e "${NOCOLOR} lets go"
curl -sSL https://get.docker.com/ | CHANNEL=stable sh
sudo usermod -aG docker ${USER}
sudo systemctl enable --now docker

