import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin = 22

GPIO.setup(pin, GPIO.OUT)
while True:
	print "LED on"
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(1)
	# print "LED off"
	# GPIO.output(pin, GPIO.LOW)