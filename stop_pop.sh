#!/bin/bash

echo "Searching for Django runserver process..."

# Find the PID of the Django runserver process
PID=$(ps aux | grep "manage.py runserver" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "No Django server running."
else
    echo "Stopping Django server (PID: $PID)..."
    kill -9 $PID
    echo "Django server stopped."
fi

#once you've made the file remember to make it executable: chmod +x ~/Desktop/stop_pop.sh
#right click on the icon the file and make sure it opens with terminal, bash, or command prompt by default

