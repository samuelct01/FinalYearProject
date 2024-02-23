import paho.mqtt.client as mqtt
import ssl
import time
import json
import random
from steps import step
import socket
 
# json object to hold current values
instructions = None

#turbine poition information
angleToMove = 0
currentRev = 0
currentAngle = 0

#saves the space in the sequence for stepper motor 
inseq = 0
# the onboard  code for controlling the turbine that communicates with the cloud 

# when message is recieved write it to global variable instructions
def on_message(client, userdata, message):
    global instructions
    message = message.payload.decode("utf-8")
    instructions = json.loads(message)
    print(f"Received message: {message}")

def on_connect(client, userdata, flags,rc):
    print("connected with result code"+str(rc))


#connect to the aws iot broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(
            ca_certs="AmazonRootCA1.pem",
            certfile="56dbe40dd150e8d4c49f6e9e5c7e092600ea0560a1317739cf49d370123db107-certificate.pem.crt",
            keyfile="56dbe40dd150e8d4c49f6e9e5c7e092600ea0560a1317739cf49d370123db107-private.pem.key",
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2
        )
client.tls_insecure_set(True)
client.connect("a2w8i53ab6a4ti-ats.iot.eu-west-2.amazonaws.com", 8883, 60)

#connecting to the weather station

socketsclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi = ""
port = 8000
socketsclient.connect((ip, port))


print('atm' + str(angleToMove))
print('cr' + str(currentRev))
print('ca' + str(currentAngle))

#loop to handle incoming messages
client.loop_start()



while True:
	

    data = {
    "direction": random.randint(0, 359),
    "speed": random.randint(5, 100),
    "currentAngle": currentAngle,
    "currentRev": currentRev
    }
    #publish data to topic
    client.publish('topic_2', json.dumps(data))
    
    #recieve data from lambda function
    client.subscribe('topic_4')


    #must allow time for subscription to be recieved
    time.sleep(3)  
    
    #if no instruction is recieved stop the program
    if instructions == None:
	    print("no message recieved")
	    break
    
	#set position data vairables to attributes from message
    angleToMove = instructions['angleToMove']
    currentRev = instructions['currentRev']
    currentAngle = instructions['currentAngle'] 
    
    print('atm' + str(angleToMove))
    print('cr' + str(currentRev))
    print('ca' + str(currentAngle))
    
    #rotate stepper motor and remember poition in step sequnece for next rotation
    inseq = step(angleToMove, inseq)
    
    #reset instructions
    instructions = None
