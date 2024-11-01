#!/bin/bash
# Install Git
sudo yum install -y git

# Clone the repository
git clone https://github.com/cadizsd/reading_test.git /home/ec2-user/reading_test

# Move to the repository directory
cd /home/ec2-user/reading_test || exit

# Set up the Python virtual environment
sudo python3 -m venv .venv
source .venv/bin/activate

# Install required dependencies
.venv/bin/pip install -r requirements.txt

# Copy the service file and enable the service
sudo cp reading.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable reading
sudo systemctl start reading
