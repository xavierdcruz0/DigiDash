# DigiDash

```
The dash, it's digi, the schedule busy
My head in a hoodie, my shorty a goodie
My cousins are crazy, my cousins like Boogie
Life is amazin', it is what it should be
```

This is a work in progress to create a virtual gauge display system for
classic cars lacking OBD support. Sensor values are read by Raspberry Pi 
ADC chip, and will be conveyed to the client device through Bluetooth.

## Dependencies

Make sure development libraries are present:

`sudo apt install build-essential`

`sudo apt install python3-dev`

`sudo apt install libbluetooth-dev`

Until Bluetooth client functionality is created, there exists a simple
Tkinter GUI to view sensor readouts and debug stuff:

`sudo apt install python3-tk`

Install Python packages:

`pip install -r requirements.txt`