from locust import User, task, between
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import ssl
import json
import random

#the code in this file was created with help from generative Ai as outlined in my report appendix  
#script for load testing the lambda function 

class MqttClient(mqtt.Client):
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(client,userdata,message):
        print("recieved" + str(message.payload.decode("utf-8")))

#class that defines the mqtt client and connecting to the database.
class MqttLocust(User):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MqttClient()
        #aws credentials
        self.client.tls_set(
            ca_certs="",
            certfile="",
            keyfile="",
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
        self.client.connect("", port=8883)

    #publishes mqtt message to aws
    @task(1)
    def sender(self):
        #each message is a random value for each variable for the algorithm  within
        message = {
            "direction": random.randint(0, 359),
            "speed": random.randint(5, 100),
            "currentAngle":random.randint(0,359),
            "currentRev": random.randint(-359,359)
        }
        topic = "topic_2"
        self.client.publish(topic, payload=json.dumps(message))

    #subscribes to the relevant mqtt topic to recieve messages 
    @task(1)
    def reciever(self):
        topic = "topic_4"
        self.client.subscribe(topic)
        self.client.on_message = MqttClient.on_message

#wait between 1-5 seconds after each task 
class MyLocust(MqttLocust):
    wait = between(1, 5)
