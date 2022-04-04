from fastapi import FastAPI
from time import sleep
from fastapi.middleware.cors import CORSMiddleware

from app.routers import fingerprint, led, rfid

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


app.include_router(led.router)
app.include_router(fingerprint.router)
app.include_router(rfid.router)
