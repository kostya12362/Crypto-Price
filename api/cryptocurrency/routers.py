import asyncio
from aiohttp import ClientSession
from typing import (
    List,
    Optional,
)
from fastapi import Depends, Request
from cryptocurrency.models import (
    Cryptocurrency,
)

from utils.client_session import client_session_dep
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from contract.schemas import (
    ContractSchemas,
)
from cryptocurrency.schemas import (
    CryptocurrencyGroupResponseSchemas,
    CryptocurrencySchemas,
)

router = InferringRouter()


@cbv(router)
class CryptocurrencyAPIView:

    @router.post('/save', response_model=CryptocurrencySchemas, response_model_exclude_none=True)
    async def cryptocurrency_save(
            self,
            data: CryptocurrencySchemas,
            request: Request,
            client_session: ClientSession = Depends(client_session_dep)
    ):
        cryptocurrency = await Cryptocurrency.create_cryptocurrency(item=data)
        if data.contracts:
            async def create_contract(contract: ContractSchemas, **kwargs):
                contract.cryptocurrencyId = kwargs['id']
                await client_session.post(
                    url=request.url_for('contract_save'),
                    json=contract.dict()
                )

            tasks = [create_contract(contract=contract, **cryptocurrency) for contract in data.contracts]
            await asyncio.gather(*tasks)
        return CryptocurrencySchemas(**cryptocurrency)

    @router.get('/list', response_model=List[CryptocurrencyGroupResponseSchemas], response_model_exclude_none=True)
    async def cryptocurrency_list(self, limit: bool = True):
        cryptocurrency = await Cryptocurrency.get_cryptocurrency(limit=limit)
        return [CryptocurrencyGroupResponseSchemas(**i) for i in cryptocurrency]

    @router.get('/group', response_model=List[CryptocurrencyGroupResponseSchemas])
    async def cryptocurrency_group(self, symbol: str):
        cryptocurrency = await Cryptocurrency.get_like_cryptocurrency(symbol=symbol)
        return [CryptocurrencyGroupResponseSchemas(**i) for i in cryptocurrency]
