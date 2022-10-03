from pydantic import BaseModel
from typing import Optional


class FiatCurrencySchemas(BaseModel):
    code: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    symbol_native: Optional[str] = None
    decimal_digits: Optional[int] = None
    name_plural: Optional[str] = None
    value: Optional[float]
