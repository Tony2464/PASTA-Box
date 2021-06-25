#!/bin/bash

# Execute the system command
nb=$1

case $nb in
    
    1)
        
    ;;
    
    2)
        sudo reboot
    ;;
    
    3)
        sudo shutdown now
    ;;
    
esac
