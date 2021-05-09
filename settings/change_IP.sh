#!/bin/bash

# Backup last ip config file
sudo cp /etc/network/interfaces /etc/network/interfaces.back
# Replace with the user settings from HMI
sudo mv /PASTA-Box/settings/ipSettings.temp /etc/network/interfaces
# Restart to take effect
sudo service networking restart