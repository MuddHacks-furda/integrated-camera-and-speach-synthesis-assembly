#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import subprocess
import requests
from gpiozero import Button

camera = PiCamera()
button = Button(3)

default = True
while True:
	while True:
		if not button.is_pressed:
			default = True
		if button.is_pressed and default:
			default = False
			break
	subprocess.call(["espeak","-s 120 -v en ","Taking Picture"])
	camera.capture('/tmp/picture.jpg')
	subprocess.call(["espeak","-s 120 -v en ","Picture taken, awaiting response"])
	#r = requests.get('http://192.168.43.35:5000/')
	#print(r.text)
	with open('/tmp/picture.jpg', 'r+b') as f:
		r = requests.post('http://192.168.43.35:5000/upload', files={'picture.jpg': f})
		subprocess.call(["rm","/tmp/picture.jpg"])
		print r.text
		if "and" in r.text:
			subprocess.call(["espeak","-s 120 -v en ","The objects are a " + r.text])
		else:
			subprocess.call(["espeak","-s 120 -v en ","The object is a " + r.text])
		#subprocess.call(["espeak","-s 120 -v en ","Made by Carrot, a subsidary of FERDA Incorporated."])
