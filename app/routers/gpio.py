from fastapi import APIRouter
from gpiozero import LED
from time import sleep
from schema import Pin
import RPi.GPIO as GPIO


router = APIRouter(tags=["GPIO Pins"])


@router.post("/turn-on")
async def turn_on_gpio_pin(pin: Pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    number = pin.number
    GPIO.setup(number, GPIO.OUT)
    GPIO.output(number, GPIO.HIGH)
    return {"data": f"Pin {number} has been turned on"}


@router.post("/turn-off")
async def turn_off_gpio_pin(pin: Pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    number = pin.number
    GPIO.setup(number, GPIO.OUT)
    GPIO.output(number, GPIO.LOW)
    return {"data": f"Pin {number} has been turned off"}


