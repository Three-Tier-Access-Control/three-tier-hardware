# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from fastapi import APIRouter, HTTPException, Response, status
import board

# import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
from schema import Fingerprint

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
import serial

uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

##################################################
# LCD

import app.routers.I2C_LCD_driver as I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()


router = APIRouter(tags=["Fingerprint"])


##################################################


@router.post("/read-fingerprint")
def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    mylcd.lcd_display_string("Waiting for fingerprint image...", 1)
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    mylcd.lcd_display_string("Templating fingerprint image...", 1)
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Finger not found")
        mylcd.lcd_display_string("Finger not found", 1)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finger not found",
        )
        # return False
    print("Searching for a match...")
    mylcd.lcd_display_string("Searching for a match...", 1)
    if finger.finger_search() != adafruit_fingerprint.OK:
        print("Finger not found")
        mylcd.lcd_display_string("Finger not found", 1)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finger not found",
        )
        # return False

    # return True
    print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    mylcd.lcd_display_string("Fingerprint match detected", 1)
    return {
        "data": {
            "msg": f"Detected #, {finger.finger_id}, with confidence, {finger.confidence}",
            "finger": finger.finger_id,
            "confidence": finger.confidence,
        }
    }


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="", flush=True)
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="", flush=True)
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="", flush=True)
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
@router.post("/enroll-fingerprint")
def enroll_finger(fingerprint: Fingerprint):
    """Take a 2 finger images and template it, then store in 'location'"""

    if (fingerprint.location > 127) or (fingerprint.location < 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enter a valid number from 1 to 127",
        )

    for fingerimg in range(1, 3):
        if fingerimg == 1:
            mylcd.lcd_display_string("Place finger on sensor...", 1)
            print("Place finger on sensor...", end="", flush=True)
        else:
            mylcd.lcd_display_string("Place same finger again...", 1)
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                mylcd.lcd_display_string("Fingerprint image taken", 1)
                break
            if i == adafruit_fingerprint.NOFINGER:
                mylcd.lcd_display_string(".", 1)
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                mylcd.lcd_display_string("Imaging error", 1)
                # return False
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Imaging error",
                )
            else:
                print("Other error")
                mylcd.lcd_display_string("Internal error", 1)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Other error",
                )
                # return False

        print("Templating...", end="", flush=True)
        mylcd.lcd_display_string("Templating fingerprint...", 1)

        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
            mylcd.lcd_display_string("Templating done!", 1)

        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                mylcd.lcd_display_string("Fingerprint image too messy", 1)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Image too messy",
                )
            elif i == adafruit_fingerprint.FEATUREFAIL:
                mylcd.lcd_display_string("Could not identify features", 1)
                print("Could not identify features")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Could not identify features",
                )
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                mylcd.lcd_display_string("Fingerprint image invalid", 1)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Image invalid",
                )
            else:
                mylcd.lcd_display_string("Internal error", 1)
                print("Other error")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Other error",
                )
            # return False

        if fingerimg == 1:
            print("Remove finger")
            mylcd.lcd_display_string("Remove finger", 1)
            # time.sleep(1) #not sure why but just remove it
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    mylcd.lcd_display_string("Creating model...", 1)

    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
        mylcd.lcd_display_string("Created...", 1)
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            mylcd.lcd_display_string("Prints did not match", 1)
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Prints did not match",
            )
        else:
            print("Other error")
            mylcd.lcd_display_string("Internal error", 1)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Other error",
            )
        # return False

    print("Storing model #%d..." % fingerprint.location, end="", flush=True)
    mylcd.lcd_display_string("Storing model...", 1)
    i = finger.store_model(fingerprint.location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        mylcd.lcd_display_string("Fingerprint stored", 1)
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
            mylcd.lcd_display_string("Bad storage location", 1)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Bad storage location",
            )
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
            mylcd.lcd_display_string("Flash storage error", 1)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Flash storage error",
            )
        else:
            print("Other error")
            mylcd.lcd_display_string("Internal error", 1)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Other error",
            )
        # return False

    return {
        "data": {
            "location": fingerprint.location,
            "msg": f"Stored fingerprint model on location {fingerprint.location}",
        }
    }


@router.delete("/delete-fingerprint")
async def delete_fingerprint(fingerprint: Fingerprint):
    if finger.delete_model(fingerprint.location) == adafruit_fingerprint.OK:
        print("Deleted!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        print("Failed to delete")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete",
        )


@router.get("/fingerprint-templates")
async def get_fingerprint_templates():
    if finger.read_templates() != adafruit_fingerprint.OK:
        # raise RuntimeError("Failed to read templates")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read templates",
        )
    print("Fingerprint templates:", finger.templates)
    return {"data": finger.templates}


##################################################


# def get_num():
#     """Use input() to get a valid number from 1 to 127. Retry till success!"""
#     i = 0
#     while (i > 127) or (i < 1):
#         try:
#             i = int(input("Enter ID # from 1-127: "))
#         except ValueError:
#             pass
#     return i


# while True:
#     print("----------------")
#     if finger.read_templates() != adafruit_fingerprint.OK:
#         raise RuntimeError("Failed to read templates")
#     print("Fingerprint templates:", finger.templates)
#     print("e) enroll print")
#     print("f) find print")
#     print("d) delete print")
#     print("----------------")
#     c = input("> ")

#     if c == "e":
#         enroll_finger(get_num())
# if c == "f":
#     if get_fingerprint():
#         print("Detected #", finger.finger_id, "with confidence", finger.confidence)
#     else:
#         print("Finger not found")
# if c == "d":
#     if finger.delete_model(get_num()) == adafruit_fingerprint.OK:
#         print("Deleted!")
#     else:
#         print("Failed to delete")
