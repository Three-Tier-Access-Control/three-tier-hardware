from fastapi import APIRouter, HTTPException, Response, status
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from schema import RFIDData

import app.routers.I2C_LCD_driver as I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()


router = APIRouter(tags=["RFID Module"])

# Read data to RFID Card
@router.get("/read-rfid-card")
async def read_rfid_card():
    try:
        reader = SimpleMFRC522()
        print("Place your tag to read...")
        mylcd.lcd_display_string("Place your card", 1)
        mylcd.lcd_display_string("for reading...", 2)
        id, text = reader.read()
        print(f"Tag read #: {id} \n Data: {text}")
        mylcd.lcd_display_string("Card has been ", 1)
        mylcd.lcd_display_string("read!", 2)
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
        mylcd.lcd_display_string("Place your card", 1)
        mylcd.lcd_display_string("to be written", 2)
        reader.write(data.text)
        print("Tag has been successfully written!")
        mylcd.lcd_display_string("Tag has been", 1)
        mylcd.lcd_display_string("written!", 2)

        return {"detail": "Tag has been successfully written!"}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()
