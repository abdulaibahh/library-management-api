from pydantic import BaseModel


class RoleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
