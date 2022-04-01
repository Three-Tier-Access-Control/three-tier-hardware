from fastapi import APIRouter
from gpiozero import LED
from time import sleep
from schema import Pin

router = APIRouter(tags=["LED"])


@router.post("/turn-on-led")
async def turn_on_led(pin: Pin):
    led = LED(pin.number)
    led.on()
    return {"data": "Turned on LED"}


@router.post("/turn-off-led")
async def turn_off_led(pin: Pin):
    led = LED(pin.number)
    led.off()
    return {"data": "Turned off LED"}

@router.post("/blink-led")
async def blink_led(pin: Pin):
    led = LED(pin.number)
    for x in range(6):
        led.on()
        sleep(1)
        led.off()
        sleep(1)
    return {"data" : "Blinked for while"}
