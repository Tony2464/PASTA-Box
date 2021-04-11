#!/usr/bin/env bash

services=$(ls | grep './*\.\(service\|timer\)')

for service in $services
do
   sudo cp -rf $service /lib/systemd/system/
done

# sudo systemctl daemon-reload

for service in $services
do
   sudo systemctl enable $service
   sudo systemctl start $service
done
