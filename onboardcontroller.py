import socket 
import time
import yaw
import json
import steps

def run_controller():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	ip_address = "192.168.0.40"
	port = 8000
	print("attempting to connect")

	client.connect((ip_address, port))
	print("connected")

	inseq = 0 # remembers the last position in the sequence of steps for maore accureate stepping
	currentRev = 0
	angleToMove = 0
	currentAngle = 0
	try:
		while True:		
			client.send("send weather data".encode("utf-8")[:1024])
			
			msg = client.recv(1024)
			msg = msg.decode("utf-8"[:1024])
					
		
			msg = json.loads(msg)
			speed = msg["speed"]
			direction = msg["direction"]
			print(str(speed) + "speed")
			print(str(direction) + "direction")
			
			print("calcualting Yaw angle...")
			currentRev, angleToMove, currentAngle = yaw.decider(speed, direction, currentAngle, currentRev)
		
			print("currentRev" + str(currentRev))
			print("atm" + str(angleToMove))
			print("current angle" + str(currentAngle))
			print("--------------------------------")
		
			print("applying rotation")
			#call stepper mottor rotation
			inseq = steps.rotate(angleToMove, inseq)	
			print(str(inseq)+"inseq")	
			time.sleep(3)
			
	except Exception as error:
		print(f"Error with client: {error}")


run_controller()
