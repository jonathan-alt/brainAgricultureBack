from pydantic import BaseModel, Field


class Message(BaseModel):
    detail: str = Field(example="Application already exists")
