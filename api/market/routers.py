from typing import (
    List,
)
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from market.schemas import (
    MarketSchemas,
)
from market.models import Market

router = InferringRouter()


@cbv(router)
class MarketAPIView:
    """
        Routers by Market
        - list
    """

    @router.get('/list', response_model=List[MarketSchemas])
    async def list_market(self):
        markets = await Market.get_markets()
        return [MarketSchemas(**market) for market in markets]
