from fastapi import APIRouter
import app.routers.I2C_LCD_driver as I2C_LCD_driver
from schema import LCDData
import time

mylcd = I2C_LCD_driver.lcd()


def print_to_lcd(first_row: str, second_row: str):
    # Clear everything first the print new
    mylcd.lcd_display_string("", 1)
    mylcd.lcd_display_string("", 2)
    time.sleep(1)
    mylcd.lcd_display_string(first_row, 1)
    mylcd.lcd_display_string(second_row, 2)


router = APIRouter(tags=["LCD Display Module"])


@router.post("/write-to-lcd")
async def write_to_lcd(data: LCDData):
    mylcd.lcd_display_string(data.text, 1)
    return {"detail": "Data successfully written on LCD"}
