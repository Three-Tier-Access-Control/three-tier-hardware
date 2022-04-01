from pydantic import BaseModel


class Pin(BaseModel):
    number: int

