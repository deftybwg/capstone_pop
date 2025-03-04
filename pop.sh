#!/bin/bash

#I made a script to keep on my Desktop so I can use POP by clicking it like an application icon from my desktop

# EDIT this line so that the script navigates to your project directory with the manage.py file in it
cd "/home/benxo/Projects/pop" || exit

# Run Django server in the background:
python3 manage.py runserver &

# Wait a moment for the server to start:
sleep 2

# Open the browser to profile once you've got an account:
open http://127.0.0.1:8000/login || xdg-open http://127.0.0.1:8000/login

#once you've made the file remember to make it executable: chmod +x ~/Desktop/pop.sh
#right click on the icon the file and make sure it opens with terminal, bash, or command prompt by default

#this will probably run in the background as a process
#to quit the app you may need to use `ps aux | grep manage.py` find its process id and `kill <process_id>` to quit
#or you can use the stop_pop.sh script I made as well


