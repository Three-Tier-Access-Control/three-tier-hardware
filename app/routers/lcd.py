from fastapi import APIRouter
import app.routers.I2C_LCD_driver as I2C_LCD_driver
from schema import LCDData
import time

mylcd = I2C_LCD_driver.lcd()


def print_to_lcd(text: str):
    mylcd.lcd_clear() # clear screen
    mylcd.lcd_display_string(text, 1)


router = APIRouter(tags=["LCD Display Module"])


@router.post("/write-to-lcd")
async def write_to_lcd(data: LCDData):
    print_to_lcd(data.text)
    return {"detail": "Data successfully written on LCD"}
