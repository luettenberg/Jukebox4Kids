import connect
import RPi.GPIO as GPIO

def init():
    GPIO.setwarnings(True)

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():

    init()

    loadPlaylist('RITS Favs (by elixir046)')
    client.setvol(5)
    #connect.playTrack(client, 'spotify:track:1ocmRsEMI6nO9d9BdQbXNI')

    while True:
        play_ = GPIO.input(17)
        prev_ = GPIO.input(22)
        next_ = GPIO.input(27)

        if play_ == False:
            connect.tooglePlay()

        elif prev_ == False:
            connect.playPrev()

        elif next_ == False:
            connect.playNext()

# Script starts here
if __name__ == "__main__":
    main()
