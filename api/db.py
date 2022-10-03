import glob
import json
import logging
import asyncio
import asyncpg
from settings import config
from network.schemas import NetworkSchemas

logging.getLogger(__name__)


class ReadNetworkMap:
    def __init__(self):
        self.file_path = './network/networks.json'

    def __call__(self, *args, **kwargs):
        with open(self.file_path, 'r') as file:
            data = json.loads(file.read())
            self._validate(data)
            return data

    @staticmethod
    def _validate(data: list):
        last: int = 0
        ln: list = []
        ls: list = []
        llu: list = []
        for i in data:
            if i['id'] - last != 1:
                print(i['id'] - last != 1, last, i['id'])
                raise Exception(f"Not consistent 'id' {i['id']}")
            ln.append(i['name']), ls.append(i['symbol']), llu.append(i['logoNetworkURL'])
            last = i['id']
        if len(set(ln)) != len(ln):
            raise Exception(f"Not valid names {[item for item in set(ln) if ln.count(item) > 1]}")
        if len(set(ls)) != len(ls):
            raise Exception(f"Not valid symbol {[item for item in set(ls) if ls.count(item) > 1]}")
        _lu = [item for item in set(llu) if llu.count(item) > 1]
        if len(set(llu)) != len(llu) and len(_lu) > 1:
            raise Exception(f"Not valid symbol {_lu}")


async def run(net: list):
    con = await asyncpg.connect(config.get_db_uri)
    for i in sorted(glob.glob("./sql/*.sql"), reverse=True):
        with open(i, 'r') as sql_script:
            await con.execute(sql_script.read())
    for i in net:
        network = NetworkSchemas(**i)
        await con.execute('''
        INSERT INTO network(id, name, symbol, block_explorer_url, rpc_node_url, chain_id, is_active, logo_url, is_contracts)
            VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (symbol) DO UPDATE SET
        logo_url = excluded.logo_url,
        block_explorer_url = excluded.block_explorer_url,
        rpc_node_url = excluded.rpc_node_url,
        cryptocurrency_id = excluded.cryptocurrency_id
        RETURNING id, name, symbol, block_explorer_url, rpc_node_url, chain_id, logo_url;''',
                          network.id, network.name, network.symbol, network.blockExplorerURL, network.rpcNodeURL,
                          network.chainId, network.isActive, network.logoNetworkURL, network.isContracts
                          )
    await con.close()


if __name__ == "__main__":
    logging.info('Init sql script to db')
    reader = ReadNetworkMap()
    networks = reader()
    asyncio.get_event_loop().run_until_complete(run(net=networks))
    logging.info('Finish run sql script')
