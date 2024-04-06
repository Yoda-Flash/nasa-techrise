import analogio
import board

adc = analogio.AnalogIn(board.A0)

while True:
  print(f'Mic raw: {adc.value}')
  print(f'Mic voltage: {adc.value * adc.reference_voltage} volts')