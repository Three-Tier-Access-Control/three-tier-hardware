from fastapi import APIRouter, HTTPException, Response, status
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from schema import RFIDData

import app.routers.I2C_LCD_driver as I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()



router = APIRouter(tags=["RFID Cards"])

# Read data to RFID Card
@router.get("/read-rfid-card")
async def read_rfid_card():
    try:
        reader = SimpleMFRC522()
        print("Place your tag to read...") 
        mylcd.lcd_display_string("Place your tag to read...")
        id, text = reader.read()
        print(f"Tag read #: {id} \n Data: {text}")
        mylcd.lcd_display_string("Tag has been read!")
        return {"data": {"uid": id, "text": text}}
    except Exception as e:
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
        mylcd.lcd_display_string("Place your tag to write...")
        reader.write(data.text)
        print("Tag has been successfully written!")
        mylcd.lcd_display_string("Tag has been successfully written!")        
        return {"detail": "Tag has been successfully written!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()
