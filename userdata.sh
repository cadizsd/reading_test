#!/bin/bash
sudo yum install -y git
sudo git clone https://github.com/cadizsd/reading_test.git
cd reading_test
sudo python3 -m venv .venv
sudo .venv/bin/pip install -r requirements.txt
sudo cp reading.service /etc/systemd/system
sudo systemctl enable reading
sudo systemctl start reading
