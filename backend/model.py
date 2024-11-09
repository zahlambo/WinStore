from pydantic import BaseModel,Field
from typing import Optional

class AddItem(BaseModel):
    name: str
    Icon: str=Field(description="icon path actually",alias='icon')
    ID: str
