# pyDerby
Python/Flask application to help manage Pinewood Derby races.

This was developed against Python 3.8.

Install requirements: 
```
pip install flask (web server)
pip install flask-bootstrap
pip install pyserial (interface to race time)
pip install Pillow (image manipulation)
pip install google-cloud-firestore (internet version)
```

Timer instructions:
- https://microwizard.com/downloads/instructions/k3_Kit_instructions.pdf

### CSV Files:
- raceSchedule.csv: This file defines all of the heats by car number. As the heats proceed, the logger class updates raceSchedule.csv with the results. The web pages read raceSchedule.csv to display the schedule and results.
- registration.csv: This file contains all of the participant names, car numbers, and group. If you edit this file, you must restart the web server/Flask.

### Python Files:
- generateRaceSchedule.py: This example program creates a raceSchedule.csv. 
- pyDerby.py: Generates the web interfaces (local instance).
- main.py: Generate the wbe interface (public instace if the Google Cloud is used)
- timerInterface.py: Listens on a serial port for results from a FastTrack timer. The serial port is hard coded. You will need to identify your serial port and update the code. There is sample code in timerInterface to get the names of available serial com ports on your computer.
- simTimer.py: This is not used during racing. simTimer is used to develop pyDerby and logs times like a race in being run without having to send cars down a real track.
- NoTimer.py: gui for situations like space derby where no timer is used
- SendResToInternet.py: uploads data to google cloud for review.

### simTimerArduino:
- Arduino boards are an inexpensive way to develop the timerInterface.py without having a race track and timer setup in your house. The application emulates the FastTrack timer by sending strings back to the host computer. You would never use at an actual event.
