import pycom
import time
from machine import Pin, ADC
from lib.dht import DHT

pycom.heartbeat(False)

pycom.heartbeat(False)
pycom.rgbled(0xFF0000)  # Red
th = DHT(Pin('P23', mode=Pin.OPEN_DRAIN), 0)
btn = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)


SoilSensorPin = 'P17'
soilPin = Pin(SoilSensorPin, mode=Pin.IN)
time.sleep(2)

adc = ADC(bits=10)
adc.vref(1260)
apin = adc.channel(attn=ADC.ATTN_11DB, pin=SoilSensorPin)

time.sleep(2)

pycom.rgbled(0x00FF00)  # Green

def btn_callback_pressed(p):
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)

btn.callback(Pin.IRQ_RISING, handler=btn_callback_pressed)

while True:
    result = th.read()
    val = apin()

    pybytes.send_signal(1, result.temperature)
    pybytes.send_signal(2, result.humidity)
    pybytes.send_signal(3, 1023 - val)
    print('sent signal {}'.format(result.temperature))
    print('sent signal {}'.format(result.humidity))
    print("Value", val)

    time.sleep(600)
