# RP2040 5V Findings
https://github.com/c1570/RP2040-5V-Findings

There has been quite a lot of discussion concerning 5V compatibility of the RP2040 microcontroller on RP Pico boards.

Rather than relying on forum postings and datasheets, I did some tests.

I used the following circuit for testing (circuit drawing thanks to [wokwi.com](https://wokwi.com/)):

![RP2040 5V testing circuit](/circuit.png)

In essence, this shorts GPIO0+1, GPIO2+3, GPIO4+5, and connects each of those pairs to 5V using a 820 ohms pullup resistor.

On the RP2040, [MicroPython](https://micropython.org) was installed along with a small [testing program](/testscript.py) that goes through GPIO states and tests whether the expected result was read by the other paired GPIO pin.

Additionally, USB power could be automatically turned on and off using a separate circuit.

Testing was carried out on a black RP2040 board with RGB LED, with an FM6211 3.3V linear voltage regulator (max 500mA) on board.
The original RP Pico uses an RT6150 3.3V buck boost voltage converter.

Standard GPIO output drive strength was used (4mA).

## Target Audience / Disclaimer

I only have passing knowledge of analog circuits.
Do your own testing.

**DO NOT** use these findings for anything commercial or any crucial applications.

These experiments were mostly motivated by retro computing applications where a failing RP2040 isn't the end of the world, and external circuity is mostly open collector with ~1k pullups.

**USE THIS INFORMATION AT YOUR OWN RISK.**

## Findings

### General

1. For the "GPIO set to input" case, pins stay at 5V due to pullups, and no current flows.
2. For the "GPIO set to output low/0V" case, pins are pulled to 0V, and current flows through the pullup into the GPIOs (to GND).
3. For the "GPIO set to output high/3.3V" case, pins are pulled to 3.3V, and current flows from 5V via the pullup resistor into the GPIO.

In the latter case, the current sourced from 5V seems to flow into IOVDD.
This can be verified by using an additional external 5V power source and connecting that to the 820 ohms resistor instead of the VBUS pin.
Then, the Pico board shows reduced USB power usage, indicating that its power is drawn via GPIOs partially.

This can become a problem if GPIO input current exceeds the RP2040 current consumption:
Depending on the IOVDD voltage regulator used on the board, IOVDD may exceed 3.3V then.

To prevent this:
* Avoid the "GPIO output 3.3V high + external 5V high" case. OR
* Add a load resistor between 3.3V and GND that can sink the maximum expected GPIO current inflow while staying below the IOVDD voltage regulator maximum load. OR
* Use a voltage regulator that can deal with reverse current. OR
* Add a voltage limiting circuit on IOVDD.

This also means:
**Do not connect low impedance (e.g., CMOS) 5V signal lines to GPIOs directly**
unless your software is foolproof (e.g., leaves GPIO output values at 0, and only ever toggles pindirs).

If in doubt, always add a resistor.

I expect internal GPIO pullups will exhibit the same behaviour but no testing has been done yet.
As internal pullups are quite weak (several kOhms), the problem will not be as apparent.
Pulldowns are not problematic as those connect to GND instead of IOVDD.

It has not been examined whether GPIO drive strength has any influence on this behaviour.

### Stress testing

There have been statements that 5V signals can be problematic on power on since then GPIO voltage can exceed VCC by quite a margin for very short times.

I tested this by automatically power cycling the testing circuit.

A 270 ohm resistor has been added between VBUS and GND to make sure onboard capacitors discharge fully between power cycles.

After 1,000,000 power cycles, no issues have been observed.

100,000 test cycles of those have been carried out at an increased USB voltage of 5.5V.

### ADC pins

No testing has been done on ADC pins yet.
Those pins have ESD protection diodes to IOVDD.
I expect the current inflow problem detailed above to be a major problem here.
Additionally, voltage on ADC pins will be capped at 3.3V regardless of the GPIO input/output setting.
This means that logic high cannot exceed 3.3V.
This may be a problem with the 5V circuity you want to talk to.

## Feedback

Please open GitHub issues for feedback.
