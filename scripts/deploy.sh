sudo systemctl stop cicd
cd /home/ubuntu/CICD_Practice2/ && git pull origin master
sudo systemctl start cicd
