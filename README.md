## Activity Tracker 

This project is an advanced, background-running Activity Tracker designed for comprehensive monitoring of user activities. It intelligently distinguishes between genuine user interactions and scripted emulators, adapts to time zone changes, and ensures seamless operation in various scenarios, including low battery, no internet connection, and firewall restrictions. Additionally, it tracks irregular mouse and keyboard inputs, ensuring accurate data capture and robust error handling.

Key Features

1. Real-Time Activity Monitoring: Seamlessly tracks user activity in the background.
2. Genuine vs. Scripted Detection: Differentiates between real user inputs and automated scripts.
3. Time Zone Adaptability: Handles time zone changes dynamically.
4. Low Battery Management: Monitors battery status and adapts performance accordingly.
5. Error Handling: Robust error management for no internet connection, firewall issues, and more.
6. Irregular Input Tracking: Captures and logs irregular mouse movements and keyboard inputs

## Installation Guide
Follow these steps to set up and run the Activity Tracker on your local machine:



1 - Install virtualenv

```bash
pip install virtualenv
```
2 - Create a Virtual Environment
```bash
virtualenv venv
```
3 - Activate the Virtual Environment
```bash
venv\Scripts\activate
```
4 - Install Project Dependencies
```bash
pip install -r requirements.txt
```

Now install all the dependencies required to run the project . 
eg:- For monitoring battery status
```bash
pip install psutil
```

Project Structure
* The project is organized into the following structure for clarity and easy navigation:
```bash
Vinove-project-main/
├── README.md
├── activity_log.log
└── myproject/
    ├── activity_log.log
    ├── db.sqlite3
    ├── error_handling.log
    ├── keyboard_activity.log
    ├── manage.py
    ├── mouse_activity.log
    ├── upload_queue.json
    ├── activity_tracker/
    │   ├── [hidden elements]
    ├── myproject/
    │   ├── [hidden elements]
    ├── screenshots/
    │   ├── [hidden elements]
    ├── templates/
        └── index.html
```
