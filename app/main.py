from fastapi import FastAPI
from time import sleep
from fastapi.middleware.cors import CORSMiddleware

from app.routers import lcd, gpio
# from app.routers import facial
# from app.routers import rfid
from app.routers import fingerprint


tags_metadata = [
    {
        "name": "LCD Display Module",
        "description": "Display text to LCD Display Module.",
    },
    {
        "name": "LED Lights",
        "description": "Turn on and off LED Lights.",
    },
    {
        "name": "RFID Module",
        "description": "Read and Write to RFID Cards.",
    },
    {
        "name": "GPIO Pins",
        "description": "Control GPIO Pins",
    },
    {
        "name": "Fingerprints Module",
        "description": "Enroll, Find and Delete Fingerprints",
    },
]

app = FastAPI(
    title="Three Tier Access Control Security System - Hardware Modules API ",
    description="REST API for Three Tier Access Control Security System Hardware",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ashley T Shumba",
        "url": "https://ashleytshumba.co.zw",
        "email": "ashleytshumba@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/api/v1/openapi.json",
    openapi_tags=tags_metadata,
)


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


app.include_router(led.router)
app.include_router(
    fingerprint.router,
    prefix="/api/v1",
)
# app.include_router(
#     rfid.router,
#     prefix="/api/v1",
# )
app.include_router(
    lcd.router,
    prefix="/api/v1",
)
app.include_router(
    gpio.router,
    prefix="/api/v1",
)


# app.include_router(
#     facial.router,
#     prefix="/api/v1",
# )
