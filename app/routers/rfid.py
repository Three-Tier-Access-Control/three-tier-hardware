from fastapi import APIRouter, HTTPException, Response, status
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from app.routers.lcd import print_to_lcd
from schema import RFIDData

from time import *


router = APIRouter(tags=["RFID Module"])


# Read data to RFID Card
@router.get("/read-rfid-card")
async def read_rfid_card():
    try:
        reader = SimpleMFRC522()
        print("Place your tag to read...")
        print_to_lcd("Place your card", "for reading...")
        id, text = reader.read()
        print(f"Tag read #: {id} \n Data: {text}")
        print_to_lcd("Card has been ", "read!")
        return {"data": {"uid": id, "text": text}}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()


# Write data to RFID Card
@router.post("/write-to-rfid-card")
async def write_to_rfid_card(data: RFIDData):
    try:
        reader = SimpleMFRC522()
        print("Now place your tag to write")
        print_to_lcd("Place your card", "to be written")
        reader.write(data.text)
        print("Tag has been successfully written!")
        print_to_lcd("Tag has been", "written!")

        return {"detail": "Tag has been successfully written!"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()
