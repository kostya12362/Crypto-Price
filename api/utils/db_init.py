from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from settings import config

TORTOISE_ORM = {
    "connections":
        {
            "default": config.get_db_uri,
        },
    "apps": {
        "models": {
            "models": [
                "cryptocurrency.models",
                "network.models",
                "contract.models",
                "fiat.models",
                "market.models",
                "price.models",
                "aerich.models",
            ],
            "default_connection": "default",
        }}
}

connect = {
    "db_url": config.get_db_uri,
    "modules": {
        "models": [
            "cryptocurrency.models",
            "network.models",
            "contract.models",
            "fiat.models",
            "market.models",
            "price.models",
        ],
    },
    "generate_schemas": True,
    "add_exception_handlers": True,
}


def setup_database(app: FastAPI):
    register_tortoise(
        app,
        **connect
    )
