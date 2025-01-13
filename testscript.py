from machine import Pin
import time

# copy as main.py to board for autostart: mpremote cp testscript.py :main.py

time.sleep_ms(10)

pins = [Pin(i, Pin.IN) for i in range(10)]

tests = [
  [Pin.IN,  0, Pin.IN,  0, 1, 1],
  [Pin.IN,  0, Pin.OUT, 0, 0, 0],
  [Pin.IN,  0, Pin.OUT, 1, 1, 1],
  [Pin.OUT, 0, Pin.IN,  0, 0, 0],
  [Pin.OUT, 0, Pin.OUT, 0, 0, 0],
  [Pin.OUT, 1, Pin.IN,  0, 1, 1],
  [Pin.OUT, 1, Pin.OUT, 1, 1, 1]
]

led = Pin(25, Pin.OUT)

passed = True

while True:
  for test in tests:
    p0_mode, p0_set, p1_mode, p1_set, p0_read_expected, p1_read_expected = test
    for p0, p1 in [(0,1),(2,3),(4,5)]:
      pins[p0].init(mode=p0_mode, value=p0_set)
      pins[p1].init(mode=p1_mode, value=p1_set)
      time.sleep_ms(1)
      if pins[p0].value() != p0_read_expected:
        print(f"Pin {p0} reading wrong value")
        passed = False
      if pins[p1].value() != p1_read_expected:
        print(f"Pin {p1} reading wrong value")
        passed = False
  if not passed:
    for _ in range(100):
      led.value(1)
      time.sleep_ms(100)
      led.value(0)
      time.sleep_ms(100)
  else:
    print("Ok")
    led.value(1)
