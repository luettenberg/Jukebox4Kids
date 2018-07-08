#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time 
import Adafruit_SSD1306 

from PIL import Image 
from PIL import ImageDraw 
from PIL import ImageFont 

import subprocess 
import threading 
import re 
import logging

class Display(threading.Thread):
    """Handles visualisation on jukebox display."""
    # Raspberry Pi pin configuration:
    RST = None # on the PiOLED this pin isnt used
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
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 2
    
    def __init__(self, gpio):
        """Initialize Display."""
        threading.Thread.__init__(self)
        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=self.RST, gpio=gpio)
        # Initialize library.
        self.disp.begin()
        self.clearDisplay()
        # Create blank image for drawing. Make sure to create image with mode '1' for 
        # 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        # Draw some shapes. First define some constants to allow easy resizing of 
        # shapes.
        padding = -2
        self.top = padding
        # Load default font.
        self.font = ImageFont.load_default()

    def clearDisplay(self):
        # Clear display.
        self.disp.clear()
        self.disp.display()

    def isHealthy(self):
        return True

    def getState(self):
        current = {'song': "none", 'state': "none", 'currentTrack': "0",
                   'trackAmount': "0", 'trackPlayed': "0:00", 'volume': "0", 
                   'trackLength': "0:00"}

	try:
	  cmd = "mpc"
	  state = subprocess.check_output(cmd, shell=True)
	except subprocess.CalledProcessError as e:
	  logging.exception("Error calling mpc.Returning default infos.")
	  return current
        
	if state is None:
	  logging.error("Mpc state could not be retrieved. Returning default")
	  return current
			
	try:
	  state = state.decode('utf-8')
	  lines = state.split("\n")
          if (len(lines) >= 3):
              pattern = re.compile("^\[(.*)\]\s+#(\d+)\/(\d+)\s+([0-5]?\d:[0-5]\d)\/([0-5]?\d:[0-5]\d).*$")
              match = pattern.match(lines[1])
              current['song'] = unicode(lines[0]).strip()
              current['volume'] = str(lines[2][7:lines[2].find("%")]).strip()
              current['state'] = str(match.group(1)).strip()
              current['currentTrack'] = str(match.group(2)).strip()
              current['trackAmount'] = str(match.group(3)).strip()
              current['trackPlayed'] = str(match.group(4)).strip()
              current['trackLength'] = str(match.group(5)).strip()
          else:
              current['volume'] = str(lines[0][7:lines[0].find("%")]).strip()
        except Exception as e:
     	  logging.exception("Error parsing State: " + state)
	
        return current

    def run(self):
        """Update Display frequently."""
        while True:
	    try:
              # Draw a black filled box to clear the image.
              self.draw.rectangle((0, 0, self.width, self.height),
                                outline=0, fill=0)
              state = self.getState()
              line1 = '[{:5}] {:>11}'.format(
                  str(state['state']).strip(),
                  str(state['currentTrack'] + "/" + state['trackAmount']).strip()
                  )
              line2 = 'Time: {:>15}'.format(
                  str(state['trackPlayed'] + '/' + state['trackLength']).strip()
                  )
              line3 = 'Volume: {:>13}'.format(str(state['volume'] + '%').strip())
              self.draw.text((self.x, self.top+2), line1,
                           font=self.font, fill=255)
              self.draw.text((self.x, self.top+12), line2,
                           font=self.font, fill=255)
              self.draw.text((self.x, self.top+22), line3,
                           font=self.font, fill=255)
              # Display image.
              self.disp.image(self.image)
              self.disp.display()
	    except Exception as e:
		logging.exception("DISPLAY - Error in main loop")
            
            if (state['state']=='playing'):
            	time.sleep(1)
	    else:
		time.sleep(10)
