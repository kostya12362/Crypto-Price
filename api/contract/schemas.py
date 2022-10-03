from typing import (
    Optional,
    List,
)
from market.schemas import MarketSchemas

from pydantic import BaseModel


class ContractSchemas(BaseModel):
    id: Optional[int] = None
    name: str
    symbol: str
    contractAddress: str
    decimals: Optional[int] = None
    blockExplorerURL: Optional[str] = None
    networkName: Optional[str] = None
    networkLogoURL: Optional[str] = None
    chainId: Optional[int] = None
    logoURL: Optional[str] = None
    rpcNodeURL: Optional[List[str]] = None
    bridge: Optional[bool] = False
    cryptocurrencyId: Optional[int] = None
    networkId: Optional[int] = None
    marketId: Optional[int] = None


class BaseContractSchemas(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    contractAddress: Optional[str] = None
    decimals: Optional[int] = None
    blockExplorerURL: Optional[str] = None
    networkName: Optional[str] = None
    networkLogoURL: Optional[str] = None
    chainId: Optional[int] = None
    rpcNodeURL: Optional[List[str]] = None
    bridge: Optional[bool] = False
    networkId: Optional[int] = None


class ContractResponseSchemas(BaseContractSchemas):
    markets: Optional[List[MarketSchemas]] = None
