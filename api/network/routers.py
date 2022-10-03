from typing import (
    List,
)
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv

from network.models import Network
from network.schemas import (
    NetworkSchemas,
)


router = InferringRouter()


@cbv(router)
class NetworkAPIView:
    """
        Routers by Market
        - list
    """

    @router.post('/list', response_model=List[NetworkSchemas])
    async def network_list(self):
        networks = await Network.get_networks()
        return [NetworkSchemas(**network) for network in networks]

    @router.get('/trigger')
    async def detect_networks(self):
        await Network.detect_network()
        return {"detail": "is processing"}
