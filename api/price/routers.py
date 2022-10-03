from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from price.models import Price

router = InferringRouter()


@cbv(router)
class PriceAPIView:

    @router.get('/detail')
    async def get_price(self, symbols: str, code_fiat: str = 'USD'):
        _s = [i.strip() for i in symbols.split(',')]
        val = await Price.get_last_value(symbols=_s, fiat=code_fiat)
        return val
