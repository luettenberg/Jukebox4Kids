#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import threading


class Display(threading.Thread):
    """Handles visualisation on jukebox display."""

    # Raspberry Pi pin configuration:
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    disp = None
    draw = None
    image = None
    font = None

    width = 0
    height = 0
    top = 0

    # Move left to right keeping track of the current x position
    # for drawing shapes.
    x = 2

    def __init__(self, gpio):
        """Initialize Display."""
        threading.Thread.__init__(self)

        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST, gpio=gpio)

        # Initialize library.
        self.disp.begin()

        self.clearDisplay()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding

        # Load default font.
        self.font = ImageFont.load_default()

    def clearDisplay(self):
        # Clear display.
        self.disp.clear()
        self.disp.display()

    def run(self):
        """Update Display frequently."""
        while True:
            # Draw a black filled box to clear the image.
            self.draw.rectangle((0, 0, self.width, self.height),
                                outline=0, fill=0)
            cmd = "mpc status | awk \'FNR == 2 {print $2}\'"
            Track = subprocess.check_output(cmd, shell=True)
            cmd = "mpc status | awk 'FNR == 2 {print $3}'"
            Current = subprocess.check_output(cmd, shell=True)
            cmd = "mpc status | awk 'FNR == 2 {print $1}'"
            State = subprocess.check_output(cmd, shell=True)
            cmd = "mpc volume | cut -d\':\' -f2"
            Volume = subprocess.check_output(cmd, shell=True)
            line1 = '{:7} {:>11}'.format(
                str(State).strip(), str(Track).strip())
            line2 = 'Time: {:>15}'.format(str(Current).strip())
            line3 = 'Volume: {:>13}'.format(str(Volume).strip())
            self.draw.text((self.x, self.top+2), line1,
                           font=self.font, fill=255)
            self.draw.text((self.x, self.top+12), line2,
                           font=self.font, fill=255)
            self.draw.text((self.x, self.top+22), line3,
                           font=self.font, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.display()

            time.sleep(1)
