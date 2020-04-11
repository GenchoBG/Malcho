import RPi.GPIO as GPIO
from time import sleep

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(2.5) # Initialization

def SetAngle(angle):
    duty = round(angle / 18.0, 1) + 2
    GPIO.output(servoPIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPIN, False)
    pwm.ChangeDutyCycle(0)

SetAngle(0)
sleep(2)
SetAngle(90)
sleep(2)
SetAngle(180)
sleep(2)

pwm.stop()
GPIO.cleanup()