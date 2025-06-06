from pydantic import BaseModel

class TokenData(BaseModel):
    username: str | None = None

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True