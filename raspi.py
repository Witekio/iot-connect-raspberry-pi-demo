# python3 shadow.py --endpoint REPLACE_ME-ats.iot.us-east-1.amazonaws.com \
# --cert REPLACE_ME-certificate.pem.crt \
# --key REPLACE_ME-private.pem.key \
# --root-ca root-CA.crt \
# --thing-name raspi \
# --shadow-property light
import RPi.GPIO as GPIO
import time
ledPin = 11

def setup():
    GPIO.setmode(GPIO.BOARD) # use Physical GPIO Numbering,
    GPIO.setup(ledPin, GPIO.OUT) # set the ledPin to OUTPUT mode
    GPIO.output(ledPin, GPIO.LOW) # make ledPin output LOW level
    print ('using pin%d'%ledPin)


def turn_on():
    GPIO.output(ledPin, GPIO.HIGH)
    print ('led turned on >>>')


def turn_off():
    GPIO.output(ledPin, GPIO.LOW)
    print ('led turned off >>>')


def destroy():
    GPIO.cleanup()
