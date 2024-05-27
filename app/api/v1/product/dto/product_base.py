from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    id: Optional[int] = Field(default=None)
    category: str
    selling_price: int
    cost_price: int
    name: str
    description: str
    barcode: str
    expiration_date: datetime
    size: str
    search_keywords: str =Field()
    user_id: Optional[int] = Field(default=None)
