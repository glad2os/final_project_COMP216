import tkinter

import paho.mqtt.client as mqtt
from time import sleep
from group_5_data_generator import Util
from group_5_gui import Display

class publisher:
    def __init__(self, delay =1, topic='COMP216'):
        self.gen = Util()
        self.client = mqtt.Client()
        self.topic = topic
        self.delay = delay

    def publish(self, times=10):
        for x in range(times):
            print(f'#{x}', end=' ' )
            self.__publish()

    def __publish(self):
        data = self.gen.get_json_data()
        print(f'{data} to broker')
        self.client.connect('localhost', 1883)
        self.client.publish(self.topic, payload=data)
        sleep(self.delay)                           #necessary
        self.client.disconnect()

pub = publisher()


pub.publish()