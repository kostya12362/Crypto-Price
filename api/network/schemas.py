from typing import (
    List,
    Optional,
    Union,
)
from pydantic import BaseModel


class NetworkSchemas(BaseModel):
    id: Optional[int] = None
    name: str
    symbol: str
    blockExplorerURL: Optional[str] = None
    rpcNodeURL: Optional[List[str]] = None
    chainId: Optional[int] = None
    cryptocurrency: Optional[Union[int, dict]] = None
    logoNetworkURL: str
    isActive: bool = True
    isContracts: bool = False
