import connect
import RPi.GPIO as GPIO
import signal
import time
import sdnotify

# Start configuration.
PLAY_GPIO = 17
PLAY_BOUNCE = 1000
PREV_GPIO = 27
PREV_BOUNCE = 500
NEXT_GPIO = 22
NEXT_BOUNCE = 500
# Stop configuration.

# Helper variable with all configured ports
channels = (PLAY_GPIO, PREV_GPIO, NEXT_GPIO)


def onExit():
    print('Play-Control exiting')
    GPIO.remove_event_detect(PLAY_GPIO)
    GPIO.remove_event_detect(NEXT_GPIO)
    GPIO.remove_event_detect(PREV_GPIO)
    GPIO.cleanup(channels)


def onTooglePlayEvent(channel):
    print('Play-Control executing onTooglePlayEvent')
    connect.tooglePlay()


def onPreviouse(channel):
    print('Play-Control executing onPreviouse')
    connect.playPrev()


def onNext(channel):
    print('Play-Control executing onNext')
    connect.playNext()


def main():
    print('Play-Control starting')

    signal.signal(signal.SIGINT, onExit)
    signal.signal(signal.SIGTERM, onExit)

    # Configure GPIO
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    # Setup Channels
    GPIO.setup(channels, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Register Callbacks
    GPIO.add_event_detect(
        PLAY_GPIO, GPIO.FALLING, callback=onTooglePlayEvent, bouncetime=PLAY_BOUNCE)
    GPIO.add_event_detect(
        PREV_GPIO, GPIO.FALLING, callback=onPreviouse, bouncetime=PREV_BOUNCE)
    GPIO.add_event_detect(
        NEXT_GPIO, GPIO.FALLING, callback=onNext, bouncetime=NEXT_BOUNCE)

    #Init Service Watchdog
    n = sdnotify.SystemdNotifier()
    n.notify('READY=1')

    print('Play-Control started')

    # Endlosschleife
    try:
        while True:
            time.sleep(0.5)
            n.notify('WATCHDOG=1')
    except Exception:
        print('Exception raised - exiting')
    onExit()


if __name__ == "__main__":
    main()
