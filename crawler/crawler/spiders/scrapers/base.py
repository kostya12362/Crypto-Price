import scrapy


class BaseSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        'AUTOTHROTTLE_START_DELAY': 0,
        'ITEM_PIPELINES': {
            'crawler.spiders.pipelines.cryptocurrency.CryptocurrencySavePipeline': 300
        },
    }
    handle_httpstatus_list = [403, 422, 500]
    MAP_SCRAPER = {
        'coinmarketcap': {
            'marketId': 1,
            'marketName': 'CoinMarketCap',
            'marketLogoURL': 'https://gateway.pinata.cloud/ipfs/QmQAGtNJ2rSGpnP6dh6PPKNSmZL8RTZXmgFwgTdy5Nz5mx',
            'marketSite': 'https://coinmarketcap.com',
        },
        'coingecko': {
            'marketId': 2,
            'marketName': 'CoinGecko',
            'marketLogoURL': 'https://static.coingecko.com/s/gecko-65456030ba03df0f83f96e18d0c8449485c1a61dbdeeb733ca69164982489d0e.svg',
            'marketSite': 'https://coingecko.com',
        },
        'exchangeratesapi': {
            'marketId': 3,
            'marketName': 'Exchange rate',
            'marketSite': 'https://exchangeratesapi.io/',
            'marketLogoURL': None
        },
        'soyfinance': {
            'marketId': 4,
            'marketName': 'Soy Finance',
            'marketLogoURL': 'https://app.soy.finance/logo.png',
            'marketSite': 'https://app.soy.finance/swap#/swap',
        },
        'contracts': (
            {
                'marketId': 1,
                'marketName': 'CoinMarketCap',
                'marketLogoURL': 'https://gateway.pinata.cloud/ipfs/QmQAGtNJ2rSGpnP6dh6PPKNSmZL8RTZXmgFwgTdy5Nz5mx',
                'marketSite': 'https://coinmarketcap.com',
                'url': 'https://api.coinmarketcap.com/data-api/v3/uniswap/all.json',
            },
            {
                'marketId': 2,
                'marketName': 'CoinGecko',
                'marketLogoURL': 'https://static.coingecko.com/s/gecko-65456030ba03df0f83f96e18d0c8449485c1a61dbdeeb733ca69164982489d0e.svg',
                'marketSite': 'https://coingecko.com',
                'url': 'https://tokens.coingecko.com/uniswap/all.json',
            },
            {
                'marketId': 5,
                'marketName': 'Uniswap Labs Extended',
                'marketLogoURL': 'https://gateway.pinata.cloud/ipfs/QmNa8mQkrNKp1WEEeGjFezDmDeodkWRevGFN8JCV7b4Xir',
                'marketSite': 'https://app.uniswap.org/#/swap?chain=mainnet',
                'url': 'https://gateway.pinata.cloud/ipfs/QmaQvV3pWKKaWJcHvSBuvQMrpckV3KKtGJ6p3HZjakwFtX',
            },
            {
                'marketId': 6,
                'marketName': 'Uniswap Labs Default',
                'marketLogoURL': 'https://gateway.pinata.cloud/ipfs/QmNa8mQkrNKp1WEEeGjFezDmDeodkWRevGFN8JCV7b4Xir',
                'marketSite': 'https://app.uniswap.org/#/swap?chain=mainnet',
                'url': 'https://tokens.uniswap.org',
            },
            {
                'marketId': 7,
                'marketName': 'Kleros Tokens',
                'marketLogoURL': 'https://cloudflare-ipfs.com/ipfs/QmRYXpD8X4sQZwA1E4SJvEjVZpEK1WtSrTqzTWvGpZVDwa/',
                'marketSite': 'https://cloudflare-ipfs.com/ipfs/QmV7k8JXit3idLU7nKKZuGNgp3yyvC5wKH3cYmGmBsMqiS/',
                'url': 'https://cloudflare-ipfs.com/ipfs/QmV7k8JXit3idLU7nKKZuGNgp3yyvC5wKH3cYmGmBsMqiS/'
            },
            {
                'marketId': 8,
                'marketName': 'Celo Token Lists',
                'marketLogoURL': 'https://raw.githubusercontent.com/jesse-sawa/celo-token-list/master/assets/celo_logo.svg',
                'marketSite': 'https://celo-org.github.io/celo-token-list/celo.tokenlist.json',
                'url': 'https://celo-org.github.io/celo-token-list/celo.tokenlist.json',
            },
            {
                'marketId': 9,
                'marketName': 'Compound',
                'marketLogoURL': 'https://raw.githubusercontent.com/compound-finance/token-list/master/assets/compound-interface.svg',
                'marketSite': 'https://raw.githubusercontent.com/compound-finance/token-list/master/compound.tokenlist.json',
                'url': 'https://raw.githubusercontent.com/compound-finance/token-list/master/compound.tokenlist.json',
            },
            {
                'marketId': 11,
                'marketName': 'Gemini Token List',
                'marketLogoURL': 'https://www.gemini.com/static/images/loader.png',
                'marketSite': 'https://www.gemini.com/uniswap/manifest.json',
                'url': 'https://www.gemini.com/uniswap/manifest.json'
            },
            {
                'marketId': 12,
                'marketName': 'Wrapped Tokens',
                'marketLogoURL': 'https://cloudflare-ipfs.com/ipfs/QmUJQF5rDNQn37ToqCynz6iecGqAmeKHDQCigJWpUwuVLN',
                'marketSite': 'https://cloudflare-ipfs.com/ipfs/QmZcSgNpUR55HpAVJcYnn382aUgfYsuEvgVCZFqCc9sWCa/',
                'url': 'https://cloudflare-ipfs.com/ipfs/QmZcSgNpUR55HpAVJcYnn382aUgfYsuEvgVCZFqCc9sWCa/'
            },
            {
                'marketId': 13,
                'marketName': 'Optimism',
                'marketLogoURL': 'https://static.optimism.io/optimism.svg',
                'marketSite': 'https://static.optimism.io/optimism.tokenlist.json',
                'url': 'https://static.optimism.io/optimism.tokenlist.json'
            },
            {
                'marketId': 14,
                'marketName': 'Roll Social Money',
                'marketLogoURL': 'https://tryroll.com/wp-content/uploads/2018/11/cropped-icon-270x270.png',
                'marketSite': 'https://app.tryroll.com/tokens.json',
                'url': 'https://app.tryroll.com/tokens.json'
            },
        )
    }
