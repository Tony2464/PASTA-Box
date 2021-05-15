#!/bin/bash

currentHostname=$(cat /etc/hostname)
sourceFile="/etc/hosts"
newHostname=$1

# Change hostname in /etc/hostname
sudo sed -i "s/$currentHostname/$newHostname/g" /etc/hostname

# Change hostname in /etc/hosts
sudo head -n -1 $sourceFile >${sourceFile}.back
sudo mv ${sourceFile}.back $sourceFile
sudo echo "127.0.1.1       "$newHostname >> $sourceFile