from pydantic import BaseModel

class PersonBoundary(BaseModel):
    first_name: str
    last_name: str
    age: int

    class Config:
        orm_mode = True
