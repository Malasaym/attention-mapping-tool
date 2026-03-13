import time
import threading
import pandas as pd
from datetime import datetime
from pynput import mouse, keyboard
import pyautogui
import os

DATA_FILE = "data/attention_log.csv"

os.makedirs("data", exist_ok=True)

last_activity_time = time.time()
current_window = None
tracking = True

last_log_time=0
LOG_INTERVAL=1
def get_active_window():
    try:
        return pyautogui.getActiveWindow().title
    except:
        return "Unknown"


def classify_attention(event):

    if event in [
        "keyboard_activity",
        "mouse_click",
        "mouse_move",
        "mouse_scroll"
    ]:
        return "Active Engagement"

    elif event == "window_switch":
        return "Attention Shift"

    elif event == "idle":
        return "Idle"

    else:
        return "Unknown"


def log_event(event):

    timestamp = datetime.now()

    try:
        window = pyautogui.getActiveWindow()
        window_title = window.title if window else "Unknown"
    except:
        window_title = "Unknown"

    attention_state = classify_attention(event)

    row = pd.DataFrame(
        [[timestamp, event, attention_state, window_title]],
        columns=["timestamp","event","attention_state","window"]
    )

    row.to_csv(
        DATA_FILE,
        mode="a",
        header=not os.path.exists(DATA_FILE),
        index=False
    )


# Keyboard listener
def on_press(key):
    global last_activity_time
    last_activity_time = time.time()
    log_event("keyboard_activity")


# Mouse events
def on_move(x, y):
    global last_activity_time
    last_activity_time = time.time()
    log_event("mouse_move")


def on_click(x, y, button, pressed):
    global last_activity_time
    if pressed:
        last_activity_time = time.time()
        log_event("mouse_click")


def on_scroll(x, y, dx, dy):
    global last_activity_time
    last_activity_time = time.time()
    log_event("mouse_scroll")


# Window switch detection
def window_tracker():

    global current_window

    while tracking:

        new_window = get_active_window()

        if new_window != current_window:
            current_window = new_window
            log_event("window_switch")

        time.sleep(1)


# Idle detection
def idle_tracker():

    global last_activity_time

    while tracking:

        idle_time = time.time() - last_activity_time

        if idle_time > 15:
            log_event("idle")

        time.sleep(5)


keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll
)

keyboard_listener.start()
mouse_listener.start()

threading.Thread(target=window_tracker, daemon=True).start()
threading.Thread(target=idle_tracker, daemon=True).start()

print("Tracking interactions in real time... Press CTRL+C to stop.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    tracking = False
    keyboard_listener.stop()
    mouse_listener.stop()
    print("Tracking stopped.")