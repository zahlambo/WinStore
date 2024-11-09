from pydantic import BaseModel,Field
from typing import Optional

class AddItem(BaseModel):
    name: str
    icon: str
    id: str
class searchItems(AddItem):
    name: Optional[str] = None
    id: Optional[str] = None
