import connect
import RPi.GPIO as GPIO


class PlayControl:

    # Start configuration.
    PLAY_GPIO = 11  # GPIO 17
    PLAY_BOUNCE = 1000
    PREV_GPIO = 13  # GPIO 27
    PREV_BOUNCE = 500
    NEXT_GPIO = 15  # GPIO 22
    NEXT_BOUNCE = 500
    # Stop configuration.

    # Helper variable with all configured ports
    channels = (PLAY_GPIO, PREV_GPIO, NEXT_GPIO)

    def __init__(self):

        print('Play-Control starting')

        # Set Mode to Board
        GPIO.setmode(GPIO.BOARD)

        # Setup Channels
        GPIO.setup(self.channels, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Register Callbacks
        GPIO.add_event_detect(
            self.PLAY_GPIO, GPIO.FALLING,
            callback=self.__onTooglePlayEvent,
            bouncetime=self.PLAY_BOUNCE)
        GPIO.add_event_detect(
            self.PREV_GPIO,
            GPIO.FALLING,
            callback=self.__onPreviouse,
            bouncetime=self.PREV_BOUNCE)
        GPIO.add_event_detect(
            self.NEXT_GPIO, GPIO.FALLING,
            callback=self.__onNext,
            bouncetime=self.NEXT_BOUNCE)

        print('Play-Control started')

    def exit(self):
        """CleanUp, should be called before program is destroyed"""
        print('Play-Control exiting')
        GPIO.remove_event_detect(self.PLAY_GPIO)
        GPIO.remove_event_detect(self.NEXT_GPIO)
        GPIO.remove_event_detect(self.PREV_GPIO)
        GPIO.cleanup(self.channels)

    def isHealthy(self):
        return True

    def __onTooglePlayEvent(self, channel):
        print('Play-Control executing onTooglePlayEvent')
        connect.tooglePlay()

    def __onPreviouse(self, channel):
        print('Play-Control executing onPreviouse')
        connect.playPrev()

    def __onNext(self, channel):
        print('Play-Control executing onNext')
        connect.playNext()
