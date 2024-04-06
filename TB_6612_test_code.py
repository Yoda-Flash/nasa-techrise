import time
import board
import digitalio
from adafruit_motor import stepper
DELAY = 0.01
STEPS = 200

coils = (
digitalio.DigitalInOut(board.D9), # A1
digitalio.DigitalInOut(board.D10), # A2
digitalio.DigitalInOut(board.D11), # B1
digitalio.DigitalInOut(board.D12), # B2
)

for coil in coils:
  coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3],
    microsteps=None)

for step in range(STEPS):
  motor.onestep()
  time.sleep(DELAY)

for step in range(STEPS):
  motor.onestep(direction=stepper.BACKWARD)
  time.sleep(DELAY)

for step in range(STEPS):
  motor.onestep(style=stepper.DOUBLE)
  time.sleep(DELAY)

for step in range(STEPS):
  motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
  time.sleep(DELAY)

for step in range(STEPS):
  motor.onestep(style=stepper.INTERLEAVE)
  time.sleep(DELAY)

for step in range(STEPS):
  motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
  time.sleep(DELAY)

motor.release()