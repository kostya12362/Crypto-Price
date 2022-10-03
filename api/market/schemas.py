from pydantic import BaseModel
from typing import (
    Optional,
)


class MarketSchemas(BaseModel):
    marketId: int
    marketName: str
    marketLogoURL: Optional[str] = None
    marketSiteURL: Optional[str] = None
