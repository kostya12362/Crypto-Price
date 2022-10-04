import uvicorn
import asyncio
from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.responses import FileResponse
from contract.routers import router as contract
from network.routers import router as network
from cryptocurrency.routers import router as cryptocurrency
from fiat.routers import router as fiat
from price.routers import router as price
from market.routers import router as market

from utils.middlewares import setup_middlewares
from utils.db_init import setup_database
from settings import config

app = FastAPI(
    title=config.APP_NAME,
    docs_url='/docs',
    redoc_url='/redoc',
    version=config.VERSION
)

if not config.DEBUG:
    print("++++++++++")
    app.servers = [{"url": config.base_path}]
    app.root_path = config.base_path


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('./favicon.ico')


app.include_router(price, prefix='/price', tags=['Price'])
app.include_router(cryptocurrency, prefix='/cryptocurrency', tags=['Cryptocurrency'])
app.include_router(network, prefix='/network', tags=['Network'])
app.include_router(contract, prefix='/contract', tags=['Contract'])
app.include_router(fiat, prefix='/fiat', tags=['Fiat'])
app.include_router(market, prefix='/market', tags=['Market'])


@app.on_event("startup")
async def startup_event():
    setattr(app.state, "client_session", ClientSession(raise_for_status=True))
    setup_middlewares(app)
    setup_database(app)


@app.on_event("shutdown")
async def shutdown_event():
    await asyncio.wait((app.state.client_session.close()), timeout=5.0)


if __name__ == "__main__":
    print(config.unicorn_config)
    uvicorn.run(**config.unicorn_config)
