from typing import (
    List,
)
from fiat.models import FiatCurrency

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fiat.schemas import (
    FiatCurrencySchemas
)

router = InferringRouter()


@cbv(router)
class FiatCurrencyAPI:

    @router.post('/list', response_model=List[FiatCurrencySchemas], tags=['Fiat'])
    async def list_network(self):
        fiats = await FiatCurrency.get_fiats()
        return [FiatCurrencySchemas(**fiat) for fiat in fiats]
