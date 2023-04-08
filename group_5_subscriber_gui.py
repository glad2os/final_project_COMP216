import paho.mqtt.client as mqtt
import json
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import MinuteLocator, DateFormatter
import matplotlib.dates as mdates

class SubscriberGUI:
    def __init__(self, broker_address='localhost', topic='COMP216', qos=0):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_address = broker_address
        self.topic = topic
        self.qos = qos
        self.root = tk.Tk()
        self.root.title("MQTT Subscriber")
        self.root.geometry("800x600")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.x_data = []
        self.y_data = []
        self.diff_data = []


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic, qos=self.qos)

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        print(f"Received message '{data}' on topic '{msg.topic}'")
        self.process_data(data)

    def process_data(self, data):
        self.x_data.append(data['time'])
        self.y_data.append(data['temperature'])
        self.diff_data.append(data['diff_temperature'])
        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y_data)
        self.ax1.set_title('Temperature')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Temperature')
        self.ax1.set_ylim([10, 26])
        # self.ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=0.01))
        # self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
        # self.ax1.xaxis.set_major_locator(MinuteLocator(interval=1))
        # self.ax1.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.ax2.clear()
        self.ax2.plot(self.x_data, self.diff_data)
        self.ax2.set_title('Temperature Difference')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Temperature Difference')
        self.fig.subplots_adjust(hspace=0.5)
        self.canvas.draw()

    def run(self):
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()
        self.root.mainloop()

sub = SubscriberGUI()
sub.run()