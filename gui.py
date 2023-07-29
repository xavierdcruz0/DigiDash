import tkinter as tk
from tkinter import ttk
from tkinter import font
import time
import math
import json
import numpy as np


from signal_reader import SignalReaderDummy, SignalReaderMCP3008


REFRESH_INTERVAL = 100 #milliseconds
HEIGHT, WIDTH = 500, 500
CONFIG_PATH = 'configs/config1.json'
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)


class Clock():
    def __init__(self, root, **kwargs):
        self.height, self.width = kwargs.get('height'), kwargs.get('width')
        self.clock_pad_amount = kwargs.get('clock_pad_amount')

        self.canvas = tk.Canvas(root, bg="black", height=self.height, width=self.width)
        clock_box = (self.clock_pad_amount*self.width,
                     self.clock_pad_amount*self.height,
                     self.width-self.clock_pad_amount*WIDTH,
                     self.height-self.clock_pad_amount*self.height)
        self.arc = self.canvas.create_arc(clock_box, start=0, extent=240, outline="grey", width=5, style='arc')

        self.needle_length = (self.width/2)-(0.1*self.width)
        self.needle = self.canvas.create_line(0,0,0,0)

        # text box config
        self.ox = self.width * 0.15
        self.oy = self.height * 0.05
        coords = np.array([self.width/2, self.height/2])
        offset = np.array([self.ox, self.oy])
        coords += offset
        coords = np.int32(coords)
        self.numerical_label = ttk.Label(
            self.canvas,
            text="hello",
            font=('Digital-7', 30))
        self.numerical_label.place(x=coords[0], y=coords[1])

    def draw_needle(self, fraction=0):
        self.canvas.delete(self.needle)
        r = self.needle_length
        phi_degrees = 240*(1-fraction)
        phi = math.radians(phi_degrees)
        line_start = np.array([self.width/2, self.height/2])
        line_end = np.array([r*math.cos(phi), -1*r*math.sin(phi)])
        line_end+=line_start
        line_start, line_end = np.int32(line_start), np.int32(line_end)
        x0,y0,x1,y1 = line_start[0], line_start[1], line_end[0], line_end[1]
        self.needle = self.canvas.create_line(x0,y0,x1,y1, width=5, fill="white")
    



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.signal_reader = SignalReaderDummy(**config)
        # self.signal_reader = SignalReaderMCP3008(**config)

        # configure the root window
        self.title('Digi')
        self.resizable(0, 0)
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self['bg'] = 'grey'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='white')

        # label
        self.label = ttk.Label(
            self,
            text=self.gauge_string(),
            font=('Digital-7', 40))

        # self.label.pack(expand=True)

        self.static_label = ttk.Label(
            self,
            text="Oil Pressure (PSI)",
            font=('Digital-7', 20))
        # self.static_label.pack(expand=True)

        # clock stuff
        # self.clock_pad_amount = 0.1
        # self.draw_clock()
        self.clock = Clock(root=self, height=HEIGHT, width=WIDTH, clock_pad_amount=0.1)
        self.clock_canvas = self.clock.canvas
        self.clock_canvas.pack(expand=True)


        # schedule an update every 1 second
        self.label.after(1000, self.update)

    def gauge_string(self):
        # return time.strftime('%H:%M:%S')
        return f"{self.signal_reader.sample_signal():.2f}"
    


    def update(self):
        """ update the label every REFRESH_INTERVAL milliseconds """

        # sample the signals from the gauge sensors
        current_value = self.signal_reader.sample_signal()

        # self.label.configure(text=self.gauge_string())

        # draw needle on clock
        MAX = 1024
        MIN = 0
        proportion = float(current_value/MAX)
        self.clock.draw_needle(proportion)

        # update numerical value on clock
        text_val = f"{current_value:07.2f}"
        self.clock.numerical_label.configure(text=text_val)

        # schedule another timer
        self.label.after(REFRESH_INTERVAL, self.update)



if __name__ == "__main__":
    clock = MainWindow()
    clock.mainloop()
