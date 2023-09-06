import RPi.GPIO as GPIO
import time
import os,sys

led_on = False
cmd='sudo sendiq -s 250000 -f 867.8625e6 -t u8 -i ~/lexus1/lexus_open.iq '

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def flashLED(count):
    for i in range(count):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(18, GPIO.LOW)
        time.sleep(.2)

def switch(ev=None):
    os.system(cmd)
    flashLED(2)
    # sys.exit()

def detectButtonPress():
    GPIO.add_event_detect(23, GPIO.FALLING, callback=switch, bouncetime=300)


def waitForEvents():
    while True:
        time.sleep(1)

def main():

    setupGPIO()
    flashLED(5)
    detectButtonPress()

    waitForEvents()

if __name__ == "__main__":
    main()