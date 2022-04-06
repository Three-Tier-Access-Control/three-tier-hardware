from fastapi import APIRouter
import drivers.I2C_LCD_driver as I2C_LCD_driver
from schema import LCDData

mylcd = I2C_LCD_driver.lcd()

router = APIRouter(tags=["LCD Display"])


@router.post("/write-to-lcd")
async def write_to_lcd(data: LCDData):
    mylcd.lcd_display_string(data.text, 1)
    return {"data": "Data successfully written on LCD"}
