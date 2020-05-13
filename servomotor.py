import RPi.GPIO as GPIO
from time import sleep

y_servo = 17
x_servo = 27
led = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(y_servo, GPIO.OUT)
GPIO.setup(x_servo, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)

pwm_y = GPIO.PWM(y_servo, 50)
pwm_y.start(2.5)

pwm_x = GPIO.PWM(x_servo, 50)
pwm_x.start(2.5)

def SetAngle(coords):
  x, y = coords

  x_duty = round(x / 18.0, 1) + 2.5
  y_duty = round(y / 18.0, 1) + 2.5

  GPIO.output(y_servo, True)
  pwm_y.ChangeDutyCycle(y_duty)
  sleep(1)
  GPIO.output(y_servo, False)
  pwm_y.ChangeDutyCycle(0)

  GPIO.output(x_servo, True)
  pwm_x.ChangeDutyCycle(x_duty)
  sleep(1)
  GPIO.output(x_servo, False)
  pwm_x.ChangeDutyCycle(0)

  GPIO.output(led, GPIO.HIGH)

def calculateAngle(x, y):
  GPIO.output(led, GPIO.LOW)
  max_angle = 45

  return (x * max_angle, y * max_angle)

try:
  while True:
    x = raw_input("x: ")
    y = raw_input("y: ")
    x_fl = float(x)
    y_fl = float(y)
    SetAngle(calculateAngle(x_fl, y_fl))

except KeyboardInterrupt:
  pwm_y.stop()
  GPIO.output(led, GPIO.LOW)
  GPIO.cleanup()