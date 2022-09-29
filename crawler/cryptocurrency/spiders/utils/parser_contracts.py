class BaseParser:
    # cryptocurrency fields
    FIELDS = [
        'name', 'symbol', 'slug', 'date_added', 'rank', 'logo_url', 'meta'
    ]
    # cryptocurrency meta fields
    FIELDS_META = [
        ('website', 'website'), ('explorers', 'explorers'), ('wallets', 'wallets'),
        ('search_on', 'searchOn'), ('community', 'community'), ('stars', 'stars'), ('source_code', 'sourceCode'),
        ('technical_doc', 'technicalDoc'), ('audit_infos', 'audit'), ('tags', 'tags'),
        ('rank', 'rank'), ('cm_id', 'cmId')
    ]
    # contracts meta fields
    FIELDS_CONTRACT = [
        ('name', 'name'), ('symbol', 'symbol'), ('name_network', 'nameNetwork'), ('decimals', 'decimals'),
        ('contract_address', 'contractAddress'), ('chain_id', 'chainId'), ('logo_url', 'logoURL'),
        ('block_explorer_url', 'blockExplorerURL'), ('rpc_node_url', 'rpcNodeURL'),
    ]
    # fiat fields
    FIAT_FIELDS = [
        'symbol', 'name', 'symbol_native', 'decimal_digits', 'code', 'name_plural', 'value'
    ]
