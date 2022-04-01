from fastapi import FastAPI
from gpiozero import LED
from time import sleep
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/blink-led")
async def blink_led(pin: int):
    led = LED(pin)
    for x in range(6):
        led.on()
        sleep(1)
        led.off()
        sleep(1)
    return {"data" : "Blinked for while"}
