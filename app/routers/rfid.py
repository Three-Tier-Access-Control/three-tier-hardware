from fastapi import APIRouter, HTTPException, Response, status
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from schema import RFIDData

reader = SimpleMFRC522()


router = APIRouter(tags=["RFID Cards"])

# Read data to RFID Card
@router.get("/read-rfid-card")
async def read_rfid_card():
    try:
        id, text = reader.read()
        print(id)
        print(text)
        return {"data": {"uid": id, "text": text}}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()


# Write data to RFID Card
@router.get("/write-to-rfid-card")
async def write_to_rfid_card(data: RFIDData):
    reader = SimpleMFRC522()
    try:
        print("Now place your tag to write")
        reader.write(data.text)
        print("Written")
        return {"data": "Card successfully written!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}",
        )
    finally:
        GPIO.cleanup()
