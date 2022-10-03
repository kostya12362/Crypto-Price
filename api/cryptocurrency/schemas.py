from typing import (
    Optional,
    List,
)
from datetime import datetime
from fastapi import HTTPException

from pydantic import (
    BaseModel,
    validator,
)
from contract.schemas import ContractSchemas, ContractResponseSchemas


class CryptocurrencySchemas(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    slug: Optional[str] = None
    date_added: Optional[datetime] = None
    logo_url: Optional[str] = None
    marketId: Optional[int] = None
    # meta data
    audit_infos: Optional[List[dict]] = None
    cm_id: Optional[str] = None
    community: Optional[List[str]] = None
    explorers: Optional[List[str]] = None
    rank: Optional[int] = None
    source_code: Optional[List[str]] = None
    stars: Optional[int] = None
    tags: Optional[List[str]] = None
    technical_doc: Optional[List[str]] = None
    website: Optional[List[str]] = None
    contracts: List[ContractSchemas] = None

    @validator('name')
    def validate_none_name(cls, value, values):
        if not value and not values['contracts']:
            return HTTPException(detail='Fields "name" required', status_code=400)
        return value


class MetaResponseSchemas(BaseModel):
    audit: Optional[List[dict]] = None
    community: Optional[List[str]] = None
    explorers: Optional[List[str]] = None
    source_code: Optional[List[str]] = None
    stars: Optional[int] = None
    tags: Optional[List[str]] = None
    technical_doc: Optional[List[str]] = None
    website: Optional[List[str]] = None


class CryptocurrencyGroupResponseSchemas(BaseModel):
    id: int
    name: Optional[str] = None
    symbol: Optional[str] = None
    slug: Optional[str] = None
    dateAdded: Optional[datetime] = None
    logoURL: Optional[str] = None
    marketId: Optional[int] = None
    cmId: Optional[int] = None
    # meta data
    meta: MetaResponseSchemas = None
    # list contracts by groups
    contracts: List[ContractResponseSchemas] = None
