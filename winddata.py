import weatherhat
import time

import socket
import threading
import json


#script to set up the weather sydtem os a sterver that the turbines can access for wind data values

sensor = weatherhat.WeatherHAT()
"""
while True:
	sensor.update(interval=3.0)
	
	currentdir = sensor.wind_direction
	currentspeed  = sensor.wind_speed
	print(currentdir)
	print(currentspeed)
	time.sleep(5)
"""

def each_client(client, address):
	try:
		while True:
			time.sleep(2)
			#pulls data from wind sensors
			sensor.update(interval=3.0)
			direction = sensor.wind_direction
			speed = sensor.wind_speed
			
			controllermsg = client.recv(1024).decode("utf-8")
			#once the client send request message package the data into a json pbject and send it 
			if controllermsg == "send weather data":
				data = {
				"direction": int(direction),
				"speed": int(speed) 
				}
				data = json.dumps(data)
				sending = data.encode("utf-8")
				client.send(sending)
	except Exception as e:
		print(f"Error with client: {e}")



def run_weather_station():
	ip = "192.168.0.40"
	port = 8000
	
	try:
		#establish the server
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((ip, port))
		
		server.listen(0)
		print(f"Listening on {ip}:{port}")
		
		while True:
			csocket, caddress = server.accept()
			print(f"connection accepted on {caddress[0]}{caddress[1]}")
			
			#create an address for the client
			
			thread = threading.Thread(target=each_client, args=(csocket, caddress))
			thread.start()
			
	except Exception as e:
		print(f"error on server: {e}")


run_weather_station()		
