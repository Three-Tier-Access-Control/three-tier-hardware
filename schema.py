from pydantic import BaseModel


class Pin(BaseModel):
    number: int

class Fingerprint(BaseModel):
    location: int

class RFIDData(BaseModel):
    text: str

class LCDData(BaseModel):
    text: str
