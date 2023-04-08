import paho.mqtt.client as mqtt
import tkinter as tk

root = tk.Tk()
class subscriber:
    def __init__(self, topic='COMP216'):
        self.client = mqtt.Client()
        self.client.on_message = subscriber.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        print(f'Subscriber listening to : {topic}\n...')

    def message_handler(client, userdat, message):  # handler for on_message
        # data = message.payload.decode("utf-8")
        # # TODO: Process data as necessary
        # self.update_graph([float(x) for x in data.split(",")])
        print(f'\n{message.topic} \n{message.payload.decode("utf-8")}')

    def block(self):
        self.client.loop_forever()

sub = subscriber()
sub.block()
