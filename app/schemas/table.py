from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    name: str = Field(..., min_length=1)
    seats: int = Field(gt=0)
    location: str = Field(..., min_length=1)


class TableRead(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    model_config = {"from_attributes": True}
