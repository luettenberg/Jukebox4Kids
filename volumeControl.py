import connect
import time
import gaugette.gpio
import gaugette.rotary_encoder
import threading


class VolumeControl(threading.Thread):

    A_PIN = 27  # GPIO 16, PIN 36, WIRING PIN 27
    B_PIN = 26  # GPIO 12, PIN 32, WIRING PIN 26
    STEP_SIZE = 2  # Volumen step size
    encoder = None

    def __init__(self):
        print("Starting PlaylistControl")
        threading.Thread.__init__(self)
        gpio = gaugette.gpio.GPIO()
        self.encoder = gaugette.rotary_encoder.RotaryEncoder.Worker(
            gpio, self.A_PIN, self.B_PIN)
        self.encoder.start()

    def isHealthy(self):
        return True

    def run(self):
        while True:
            delta = self.encoder.get_steps()
            if delta != 0:
                step = self.STEP_SIZE if delta > 0 else (-1 * self.STEP_SIZE)
                connect.changeVolume(step)
            else:
                time.sleep(0.05)
