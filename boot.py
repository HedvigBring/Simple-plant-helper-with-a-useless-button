from network import WLAN
import machine

wlan = WLAN(mode=WLAN.STA)

wlan.connect(ssid='wifi name here', auth=(WLAN.WPA2, 'password'))
print("Connecting...")
while not wlan.isconnected():
    machine.idle()
print("WiFi connected succesfully")
print(wlan.ifconfig())
