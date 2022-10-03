from tortoise import (
    Model,
    fields,
    transactions,
)

from utils.db_extract import db_extract


class FiatCurrency(Model):
    id = fields.IntField(pk=True, index=True)
    symbol = fields.CharField(max_length=128, null=True)
    name = fields.CharField(max_length=128, null=True)
    symbol_native = fields.CharField(max_length=128, null=True)
    decimal_digits = fields.IntField(null=True)
    code = fields.CharField(max_length=10, unique=True)
    name_plural = fields.CharField(max_length=128, null=True)
    value = fields.FloatField()
    market = fields.ForeignKeyField('models.Market', null=True, on_delete=fields.CASCADE)

    class Meta:
        table = "fiat"

    @classmethod
    async def get_fiats(cls):
        async with transactions.in_transaction("default") as conn:
            val = await conn.execute_query_dict(
                '''
                    SELECT * from "fiat";
                ''', ())
        return db_extract(val, to_list=True)
