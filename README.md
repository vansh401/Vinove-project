Activity Tracker 

This project is an advanced activity tracker designed to run in the background, monitoring and capturing user activities. It differentiates between genuine user inputs and script-based activity emulators, tracks time zone changes, handles low battery situations, and provides robust error handling for scenarios like no internet connection and firewall restrictions. It also handles irregular mouse movements and keyboard inputs .

## Installation

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
