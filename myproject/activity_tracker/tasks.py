import os
import json
import requests
import time
import logging
from threading import Thread
from datetime import datetime
import pytz
import math
import pyautogui
from pynput import keyboard
from PIL import Image, ImageGrab
import cv2
import numpy as np
import pytesseract
import psutil

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuration Settings
THRESHOLD_DISTANCE = 100
SUSPICIOUS_MOVEMENT_COUNT = 5
CAPTURE_SCREENSHOTS = True
LOGGING_INTERVAL = 1
SCREENSHOT_INTERVAL = 30
LOW_BATTERY_THRESHOLD = 20

# File paths for different logs
MOUSE_LOG_FILE = "mouse_activity.log"
KEYBOARD_LOG_FILE = "keyboard_activity.log"
TIMEZONE_LOG_FILE = "timezone_activity.log"
UPLOAD_LOG_FILE = "error_handling.log"
QUEUE_FILE = "upload_queue.json"
ACTIVITY_LOG_FILE = "activity_log.log"
SCREENSHOT_DIR = "screenshots"

# Set up logging
logging.basicConfig(filename=UPLOAD_LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def get_current_timezone():
    """Return the current timezone of the system."""
    return datetime.now().astimezone().tzinfo

def log_timezone_change(old_tz, new_tz):
    """Log the timezone change."""
    message = f"Time zone changed from {old_tz} to {new_tz}."
    with open(TIMEZONE_LOG_FILE, 'a') as tz_log_file:
        tz_log_file.write(f"{message} (New TZ: {new_tz})\n")

def log_activity(message, log_file=ACTIVITY_LOG_FILE):
    """Log activity messages to a specified file."""
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")

def calculate_distance(pos1, pos2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

def is_suspicious_movement(distance, threshold):
    """Determine if the movement is suspicious based on the threshold."""
    return distance > threshold

def take_screenshot():
    """Capture and save the screen."""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{int(time.time())}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    screenshot.save(filepath)
    
    log_activity(f"Screenshot saved: {filename}", ACTIVITY_LOG_FILE)
    return filepath

def track_mouse_movement():
    """Track mouse movement and detect irregular behavior."""
    previous_position = pyautogui.position()
    suspicious_movements = 0
    while True:
        current_position = pyautogui.position()
        distance = calculate_distance(previous_position, current_position)
        if distance > 0:
            log_activity(f"Mouse moved to {current_position} - Distance: {distance:.2f}", MOUSE_LOG_FILE)
            previous_position = current_position
            if is_suspicious_movement(distance, THRESHOLD_DISTANCE):
                suspicious_movements += 1
                log_activity("Suspicious movement detected!", MOUSE_LOG_FILE)
                if suspicious_movements >= SUSPICIOUS_MOVEMENT_COUNT:
                    log_activity("Scripted activity detected!", MOUSE_LOG_FILE)
                    if CAPTURE_SCREENSHOTS:
                        take_screenshot()
                    suspicious_movements = 0
        else:
            log_activity("Mouse hasn't moved", MOUSE_LOG_FILE)
        time.sleep(LOGGING_INTERVAL)

def on_press(key):
    try:
        log_activity(f'Key {key.char} pressed', KEYBOARD_LOG_FILE)
    except AttributeError:
        log_activity(f'Special Key {key} pressed', KEYBOARD_LOG_FILE)

def on_release(key):
    log_activity(f'Key {key} released', KEYBOARD_LOG_FILE)
    if key == keyboard.Key.esc:  # Stop listener
        return False

def start_keyboard_listener():
    """Start listening for keyboard events."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def monitor_timezone_changes():
    """Monitor system time zone changes."""
    current_tz = get_current_timezone()

    while True:
        time.sleep(5)  # Check every 5 seconds
        new_tz = get_current_timezone()

        if new_tz != current_tz:
            log_timezone_change(current_tz, new_tz)
            current_tz = new_tz

def is_connected():
    """Check if the system is connected to the internet."""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def queue_data(data):
    """Queue data to be uploaded later."""
    if not os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'w') as file:
            json.dump([], file)

    with open(QUEUE_FILE, 'r+') as file:
        queue = json.load(file)
        queue.append(data)
        file.seek(0)
        json.dump(queue, file)

def upload_data(data):
    """Upload data to the server."""
    try:
        # Replace with your server URL
        response = requests.post("https://yourserver.com/upload", json=data)
        response.raise_for_status()
        log_activity("Data uploaded successfully.", UPLOAD_LOG_FILE)
    except requests.RequestException as e:
        log_activity(f"Failed to upload data: {e}", UPLOAD_LOG_FILE)
        queue_data(data)

def process_queue():
    """Process the queued data when internet is available."""
    if not os.path.exists(QUEUE_FILE):
        return

    with open(QUEUE_FILE, 'r+') as file:
        queue = json.load(file)
        if not queue:
            return

        for data in queue:
            upload_data(data)

        # Clear the queue after processing
        file.seek(0)
        file.truncate()
        json.dump([], file)

def data_upload_worker():
    """Continuously check for data upload and process queued data."""
    data = {"sample": "This is a test data"}  # Replace with actual data

    while True:
        if is_connected():
            upload_data(data)
            process_queue()
        else:
            log_activity("No internet connection. Data queued.", UPLOAD_LOG_FILE)
            queue_data(data)
        time.sleep(10)  # Retry every 10 seconds

def check_battery_status():
    """Check the battery status and return battery percentage."""
    battery = psutil.sensors_battery()
    if battery is not None:
        return battery.percent
    else:
        return None

def log_low_battery(battery_percent):
    """Log the low battery event."""
    message = f"Low battery detected: {battery_percent}% remaining. Suspending activity tracking to save power."
    logging.warning(message)
    print(message)

def monitor_battery():
    """Monitor the battery level and suspend activity tracking if the battery is low."""
    while True:
        battery_percent = check_battery_status()

        if battery_percent is not None:
            if battery_percent <= LOW_BATTERY_THRESHOLD:
                log_low_battery(battery_percent)
                suspend_activity_tracking()
            else:
                log_activity(f"Battery level is sufficient: {battery_percent}%")

        time.sleep(60)  # Check battery status every 60 seconds

def suspend_activity_tracking():
    """Suspend activity tracking due to low battery."""
    message = "Activity tracking has been suspended due to low battery."
    logging.info(message)
    print(message)
    # Add the logic to suspend activity tracking here (e.g., stop tracking functions, etc.)

def start_services():
    """Start all services in separate threads."""
    mouse_thread = Thread(target=track_mouse_movement)
    keyboard_thread = Thread(target=start_keyboard_listener)
    timezone_thread = Thread(target=monitor_timezone_changes)
    data_upload_thread = Thread(target=data_upload_worker)
    battery_monitor_thread = Thread(target=monitor_battery)

    mouse_thread.start()
    keyboard_thread.start()
    timezone_thread.start()
    data_upload_thread.start()
    battery_monitor_thread.start()

    mouse_thread.join()
    keyboard_thread.join()
    timezone_thread.join()
    data_upload_thread.join()
    battery_monitor_thread.join()

