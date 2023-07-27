#!   /bin/bash -e

RED='\033[0;31m'  
NOCOLOR='\033[0m'


# Create Project Structure
echo -e "${RED}create project structure"
if [ -d "/opt/docker/fine-dust-measurement" ]
then
echo -e "${RED} directory already available"
else
echo -e "${RED} directory does not exist create directory"
echo -e "${NOCOLOR} lets go"
sudo mkdir /opt/docker/fine-dust-measurement
fi

# Install Requirements
echo -e "${RED}install dependencies and requirements"
echo -e "${NOCOLOR} lets go"
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt install python3 python3-pip nano curl git -y

echo -e "${RED}install pip requirements"
echo -e "${NOCOLOR} lets go"
sudo pip install -r requirements.txt

# Install docker
echo -e "${RED}install docker"
echo -e "${NOCOLOR} lets go"
curl -sSL https://get.docker.com/ | CHANNEL=stable sh
sudo systemctl enable --now docker

# Install Docker-Compose
echo -e "${RED}install docker-compose"
echo -e "${NOCOLOR} lets go"
LATEST=$(curl -Ls -w %{url_effective} -o /dev/null https://github.com/docker/compose/releases/latest) && LATEST=${LATEST##*/} && >
chmod +x /usr/local/bin/docker-compose