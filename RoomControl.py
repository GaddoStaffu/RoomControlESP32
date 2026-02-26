import pystray
from pystray import MenuItem as item
from PIL import Image
import requests
import threading

ESP_IP = "192.168.1.126"

def send_command(command):
    try:
        requests.get(f"http://{ESP_IP}/{command}", timeout=2)
    except:
        print("ESP32 not reachable")

def light_on(icon, item):
    threading.Thread(target=send_command, args=("lighton",)).start()

def light_off(icon, item):
    threading.Thread(target=send_command, args=("lightoff",)).start()

def fan_on(icon, item):
    threading.Thread(target=send_command, args=("fanon",)).start()

def fan_off(icon, item):
    threading.Thread(target=send_command, args=("fanoff",)).start()

def exit_app(icon, item):
    icon.stop()

image = Image.new("RGB", (64, 64), "black")

menu = (
    item("Light ON", light_on),
    item("Light OFF", light_off),
    item("Fan ON", fan_on),
    item("Fan OFF", fan_off),
    item("Exit", exit_app),
)

icon = pystray.Icon("RoomControl", image, "Room Control", menu)
icon.run()