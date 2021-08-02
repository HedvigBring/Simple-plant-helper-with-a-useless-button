# Simple-plant-helper-with-a-useless-button
Humidity, temperature, soil moisture and a button that makes the led go wild. 

## Tutorial on how to build a temperature, humidity and soil moisture sensor, with an additional disco button

### Disco Plant Sensor
by: Hedvig Bring Sellin
hb222uc

### Project Overview

This tutorial will describe how to build a device that reads and presents values pertaining to plant health.
With a bit of experience it should take no longer than 2 hours to complete, for a beginner you might need longer to get the setup correct.

### Objective

I decided on this particular project to be able to keep better track of my plants and their needs. Having clear readings and access to past data will make it easier to determine what the plants need and what they thrive from. To facilitate this in the best way possible, I chose to monitor temperature, air humidity and soil moisture, as these three are vital for a lot of plants. The device should give better insight for people who are struggling with knowing when to water their plants, or why their plants are dying in general. 

### Material

| Thing         | Description         | Price (link) |
| ------------- |:-------------:| -----:|
| LoPy4     | micro controller | (part of bundle) [949 SEK](https://www.electrokit.com/produkt/lnu-1dt305-tillampad-iot-lopy4-and-sensors-bundle/) |
| Pycom v3.1    | expansion board      |   (part of bundle) [949 SEK](https://www.electrokit.com/produkt/lnu-1dt305-tillampad-iot-lopy4-and-sensors-bundle/) |
| Breadboard | connection device     | (part of bundle) [949 SEK](https://www.electrokit.com/produkt/lnu-1dt305-tillampad-iot-lopy4-and-sensors-bundle/) |
| Jumper Wire | male-to-male     | (part of bundle) [949 SEK](https://www.electrokit.com/produkt/lnu-1dt305-tillampad-iot-lopy4-and-sensors-bundle/) |
| DHT11 | Digital humidity and temperature sensor    | (part of sensor bundle) [299 SEK](https://www.electrokit.com/produkt/sensor-kit-26-moduler/) |
| Key Switch Module | Push button that outputs a high signal when pressed   | (part of sensor bundle) [299 SEK](https://www.electrokit.com/produkt/sensor-kit-26-moduler/) |
| Jumper Wire | male-to-female    | (part of sensor bundle) [299 SEK](https://www.electrokit.com/produkt/sensor-kit-26-moduler/) |
| Soil moisture sensor |      | [29 SEK](https://www.electrokit.com/produkt/jordfuktighetssensor/) |

I chose to work with the Pycom LoPy4 partly because it was the recommended one for the course, but also because their [documentation](https://docs.pycom.io) is very good for beginners in IoT. It provides all the necessary functionality for the intended project. 

### Computer setup

I went with [Visual Studio Code](https://code.visualstudio.com) (henceforth called VSCode) in this project since I have previous experience with this particular IDE. VSCode has a plugin called Pymakr that allows us to have a REPL console in the terminal of VSCode, this can be found under the Extensions tab. The REPL console is where we upload the code to the device, simply using the 'upload' button at the bottom.

Another extension that might be useful is the Python language mode, this helps with intellisense.

### Putting the components together

I've put all my sensors on the breadboard, which is connected to the pycoms 3.3V power and ground. I chose to use 3.3 for all the sensors, including ones that normally would run on on 5V, since they seem to work equally well at a lower voltage (at least for this project). 

Below is a fritzing diagram showing how everything is connected. The Soil Mositure sensor needed an ADC channel, this is important to keep in mind when choosing an appropriate pin. 

![Fritzing image](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/PlantButton_bb.png)

Since all the sensors I used had built in resistors, no extra resistors were used. 

This setup with the breadboard is mainly for development purposes, however the expansion board can also be connected to a normal socket via a USB connector. To make the creation easier to work with and also easier to move around, I printed a ![small case](https://github.com/HedvigBring/Pycom-Breadboard-Case) to hold the breadboard and expansion board.

### Platform

I've used [Pybytes](https://pybytes.pycom.io) as a platform, it is free, easy to use and also provides charts for easy reading of the received data. This cloud solution saves all the sent data for a month, which is more than enough for this prototype. For a more developed device, one might want to look into spending some money on a solution that saves data indefinitely.

### The Code

While I normally like to keep things modular, the code needed for this project was quite minimal so the bulk of it is in the [main.py file.](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/main.py) 

The main functionality, the reading of the sensors runs through while-loop that reads the values and sends them to pybytes (more on this later).

For the button I had to make a callback function, since it needs to interrupt the while loop to do it's thing, and then allow the program to return to the while loop:

```
def btn_callback_pressed(p):
    pycom.rgbled(0xFF0000)  # Red
    time.sleep(1)
    pycom.rgbled(0x0000FF)  # Blue
    time.sleep(1)
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)

btn.callback(Pin.IRQ_RISING, handler=btn_callback_pressed)
```

The callback is sent to trigger when it detects a rise in the input from the button, it then goes through some colours and returns to normal. This button is going to have a different functionality further on, but since I haven't gotten that far yet, it serves as a disco button for now. 

The setup of the channels and the imports can be found in the [main.py file.](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/main.py)

It connects to the wifi in the [boot.py file](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/boot.py). 
Since the device is only meant for indoor/home use, the wifi should provide sufficient connection provided the home isn't too vast.

The only file in my lib folder is dht.py, which is providing functionality for the DHT11 sensor so that it provides relevant data. For simplicity's sake I used an [existing dht file for this.](https://github.com/iot-lnu/applied-iot/blob/master/sensor-examples/DHT11%20%26%20DHT22%20-%20Humidity%20%26%20Temperature%20Sensor/lib/dht.py)

### Transmitting the data

As mentioned above I used wifi for the data transmission and the pybytes library is used for sending the data to pybytes. This is very simple once you've [provisioned your device for use with pybytes](https://docs.pycom.io/pybytes/gettingstarted/).
```
while True:
    result = th.read()
    val = apin()

    pybytes.send_signal(1, result.temperature)
    pybytes.send_signal(2, result.humidity)
    pybytes.send_signal(3, 1023 - val)
    print('sent signal {}'.format(result.temperature))
    print('sent signal {}'.format(result.humidity))
    print('sent signal {}'.format(1023 - val))

    time.sleep(600)
```
It sleeps for 600 seconds to only send the data every half hour. 

### Presenting the Data

The data is saved for up to a month, and it is saved when it's sent, which in this case means every half hour. Pybytes provide several different types of graphs to use to visualise the data, I have chosen line charts as I think they work best for the intended purposes.

![graphs](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/graphs.JPG)

![temperature](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/graphs/temperature.png)
![humidity](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/graphs/humidity.png)
![humidity](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/graphs/soilmoisture.png)

### Finalizing the Design

The soil sensor I used was put into my Dragon Blood tree seen below: 

![soil probe](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/Probe.jpg)
![dragonblood](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/plant.jpg)

And the final device + breadboard looks like this:

![device](https://github.com/HedvigBring/Simple-plant-helper-with-a-useless-button/blob/main/device.jpg)

While the finished thing works as intended, I also intend to further develop it. The end goal is to connect it to a battery to make it portable, and then do the readings when you push the button, instead of continously every half our as it does now. This would allow me to use the device on  several plants and I could check the soil of each one to see if they need water or not. Overall I am happy with the result, but eager to improve it.

I had never worked with IoT devices before so this gave an exciting insight into the possibilites. While the project I choose is not the most complex one, I felt it was a nice, soft introduction to the topic, and something to build upon in the future.
