from datetime import datetime
from typing import (
    Optional,
)
from pydantic import BaseModel


class CryptocurrencyPriceSchemas(BaseModel):
    date_time: Optional[datetime] = None
    price: Optional[float] = None
