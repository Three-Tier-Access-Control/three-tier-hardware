# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

from fastapi import APIRouter, HTTPException, Response, status
import board

# import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
from app.routers.lcd import print_to_lcd
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

from time import *


router = APIRouter(tags=["Fingerprints Module"])


##################################################


@router.get("/read-fingerprint")
def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    print_to_lcd("Place your ", "finger...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    print_to_lcd("Templating your", "fingerprint...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Finger not found")
        print_to_lcd("Finger not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finger not found",
        )
        # return False
    print("Searching for a match...")
    print_to_lcd("Searching for a", "match...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        print("Finger not found")
        print_to_lcd("Finger not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finger not found",
        )
        # return False

    # return True
    print("Detected #", finger.finger_id, "with confidence", finger.confidence)
    print_to_lcd("Fingerprint", "match found!")
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
            print_to_lcd("Place finger on", "sensor...")
            print("Place finger on sensor...", end="", flush=True)
        else:
            print_to_lcd("Place same ", "finger again...")
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                print_to_lcd("Fingerprint image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print_to_lcd(".")
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                print_to_lcd("Imaging error")
                # return False
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Imaging error",
                )
            else:
                print("Other error")
                print_to_lcd("Internal error")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Other error",
                )
                # return False

        print("Templating...", end="", flush=True)
        print_to_lcd("Templating your", "fingerprint...")

        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
            print_to_lcd("Templating done!")

        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                print_to_lcd("Fingerprint image", "too messy")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Image too messy",
                )
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print_to_lcd("Could not ", "identify features")
                print("Could not identify features")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Could not identify features",
                )
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                print_to_lcd("Fingerprint image", "invalid")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Image invalid",
                )
            else:
                print_to_lcd("Internal error")
                print("Other error")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Other error",
                )
            # return False

        if fingerimg == 1:
            print("Remove finger")
            print_to_lcd("Remove finger")
            # time.sleep(1) #not sure why but just remove it
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="", flush=True)
    print_to_lcd("Creating model...")

    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
        print_to_lcd("Created...")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            print_to_lcd("Prints did not", "match")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Prints did not match",
            )
        else:
            print("Other error")
            print_to_lcd("Internal error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Other error",
            )
        # return False

    print("Storing model #%d..." % fingerprint.location, end="", flush=True)
    print_to_lcd("Storing model...")
    i = finger.store_model(fingerprint.location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        print_to_lcd("Fingerprint stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
            print_to_lcd("Bad storage", "location")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Bad storage location",
            )
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
            print_to_lcd("Flash storage", "error")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Flash storage error",
            )
        else:
            print("Other error")
            print_to_lcd("Internal error")
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
