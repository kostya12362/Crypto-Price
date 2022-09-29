
class BaseParser:

    FIELDS_CONTRACT = [
        ('name', 'name'), ('symbol', 'symbol'), ('name_network', 'networkName'), ('decimals', 'decimals'),
        ('contract_address', 'contractAddress'),
        ('chain_id', 'chainId'), ('logo_url', 'logoURL'), ('block_explorer_url', 'blockExplorerURL'),
        ('rpc_node_url', 'rpcNodeURL'), ('logo_url_network', 'networkLogoURL'),
    ]
    FIELDS = [
        'name', 'symbol', 'slug', 'date_added', 'rank', 'logo_url', 'website', 'explorers', 'wallets', 'search_on',
        'community', 'stars', 'source_code', 'technical_doc',
        'audit_infos', 'tags', 'rank', 'cm_id'
    ]
    FIAT_FIELDS = [
        'symbol', 'name', 'symbol_native', 'decimal_digits', 'code', 'name_plural', 'value'
    ]
