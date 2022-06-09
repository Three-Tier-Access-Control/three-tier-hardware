from pydantic import BaseModel


class Pin(BaseModel):
    number: int

class Fingerprint(BaseModel):
    location: int

class RFIDData(BaseModel):
    employee_id: str

class LCDData(BaseModel):
    text: str
