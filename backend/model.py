from pydantic import BaseModel,Field
from typing import Optional

class AddItem(BaseModel):
    name: str
    icon: str
    id: str
