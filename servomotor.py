import RPi.GPIO as GPIO
from time import sleep

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(2.5) # Initialization

def SetAngle(angle):
    duty = round(angle / 18.0, 1) + 2.5
    print(round(angle/18.0, 1))
    GPIO.output(servoPIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPIN, False)
    pwm.ChangeDutyCycle(0)

try:
  while True:
    i = 45
    while i < 90:
      SetAngle(i)
      print(i)
      sleep(1)
      i+=1

except KeyboardInterrupt:
  pwm.stop()
  GPIO.cleanup()