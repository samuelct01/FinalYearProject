import time
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import ssl
import json
import _thread as thread
import random


#script to publish and subscribe to messages MQTT from the cloud
#Make sure keys and certificates are changed and in the same directory when running
def on_connect(client, userdata, flags,rc):
    print("connected with result code"+str(rc))

def on_message(client,userdata,message):
    print("recieved" ,str(message.payload.decode("utf-8")))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs="./AmazonRootCA1.pem", certfile="./56dbe40dd150e8d4c49f6e9e5c7e092600ea0560a1317739cf49d370123db107-certificate.pem.crt", keyfile="./56dbe40dd150e8d4c49f6e9e5c7e092600ea0560a1317739cf49d370123db107-private.pem.key", tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a2w8i53ab6a4ti-ats.iot.eu-west-2.amazonaws.com", 8883, 60)
#client.subscribe("topic_4")





def sendmessage(placehold):
    while (True):
        client.subscribe("topic_4")
        data = {
        "direction": random.randint(0, 359),
        "speed": random.randint(5, 100),
        "currentAngle": random.randint(0, 359),
        "currentRev": random.randint(-359, 359)
            }
        message = json.dumps(data)    
        client.on_message = on_message
        client.publish("topic_2", payload=message, qos=0, retain=False)
        print("message was published")

        #instructions = subscribe.simple("topic_4 ", hostname="a2w8i53ab6a4ti-ats.iot.eu-west-2.amazonaws.com")
        #print(instructions.payload)

        time.sleep(3)

thread.start_new_thread(sendmessage,("Create message Thread",))
client.loop_forever()
