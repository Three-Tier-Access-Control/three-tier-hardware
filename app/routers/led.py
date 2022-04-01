from fastapi import APIRouter
from gpiozero import LED
from time import sleep
from schema import Pin
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)



router = APIRouter(tags=["LED"])


@router.post("/turn-on-led")
async def turn_on_led(pin: Pin):
    GPIO.output(pin.number, GPIO.HIGH)
    return {"data": "Turned on LED"}


@router.post("/turn-off-led")
async def turn_off_led(pin: Pin):
    GPIO.output(pin.number, GPIO.LOW)
    return {"data": "Turned off LED"}

@router.post("/blink-led")
async def blink_led(pin: Pin):
    GPIO.output(pin.number, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin.number, GPIO.LOW)
    sleep(1)
    return {"data" : "Blinked for a second"}
