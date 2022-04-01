from pydantic import BaseModel


class Pin(BaseModel):
    number: int

class Fingerprint(BaseModel):
    location: int

