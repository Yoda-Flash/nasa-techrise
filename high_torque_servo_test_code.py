import time

import board
import pwmio
from adafruit_motor import servo

pwm = pwmio.PWMOut(board.D5, frequency=50)

servo = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

while True:
  servo.angle = 0
  time.sleep(0.5)
  servo.angle = 90
  time.sleep(0.5)
  servo.angle = 180
  time.sleep(0.5)