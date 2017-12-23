import connect
import time
import gaugette.gpio
import gaugette.rotary_encoder
import sdnotify

A_PIN = 27  # GPIO 16, PIN 36, WIRING PIN 27
B_PIN = 26  # GPIO 12, PIN 32, WIRING PIN 26
STEP_SIZE = 2  # Volumen step size

gpio = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(gpio, A_PIN, B_PIN)
encoder.start()

#Init Service Watchdog
n = sdnotify.SystemdNotifier()
n.notify('READY=1')

while True:
    delta = encoder.get_steps()
    if delta != 0:
        connect.changeVolume(STEP_SIZE if delta > 0 else (-1 * STEP_SIZE))
    else:
        time.sleep(0.05)

    n.notify('WATCHDOG=1')
