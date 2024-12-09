import asyncio
import itertools

import orjson
import ciso8601

from core.coingecko import CoinGeckoV3Client
from core.data import CoinGecko, Config
from core.database import async_session
from models.controllers.market import MarketCoinsController


async def update_market_data() -> None:
    client = CoinGeckoV3Client(api_key=CoinGecko.api_key.to_string())
    session = async_session()
    market_coins_controller = MarketCoinsController(session)
    market_coins = await market_coins_controller.get_all()
    coins_pages = (len(market_coins) // 250) + 1

    async def fetch_market_coins(page: int) -> list[dict]:
        async with asyncio.Semaphore(30):
            return await (await client.markets(per_page=250, page=page)).json(
                loads=orjson.loads,
            )

    coins_market_tasks = [
        asyncio.create_task(fetch_market_coins(coins_page + 1))
        for coins_page in range(coins_pages)
    ]
    coins_market = await asyncio.gather(*coins_market_tasks)
    coins_market = list(itertools.chain.from_iterable(coins_market))
    coins_market = [
        (
            {
                "id": coin_market.get("id"),
                "symbol": coin_market.get("symbol"),
                "current_price": coin_market.get(
                    "current_price",
                    0.00,
                ),
                "market_cap": coin_market.get(
                    "market_cap",
                    0.00,
                ),
                "price_change_24h": coin_market.get(
                    "price_change_24h",
                    0.00,
                ),
                "price_change_percentage_24h": coin_market.get(
                    "price_change_percentage_24h",
                    0.00,
                ),
                "market_cap_change_24h": coin_market.get(
                    "market_cap_change_24h",
                    0.00,
                ),
                "market_cap_change_percentage_24h": coin_market.get(
                    "market_cap_change_percentage_24h",
                    0.00,
                ),
                "ath": coin_market.get(
                    "ath",
                    0.00,
                ),
                "ath_change_percentage": coin_market.get(
                    "ath_change_percentage",
                    0.00,
                ),
                "ath_date": ciso8601.parse_datetime(
                    coin_market.get("ath_date", "2024-01-01T00:00:00Z"),
                ),
                "atl": coin_market.get(
                    "atl",
                    0.00,
                ),
                "atl_change_percentage": coin_market.get(
                    "atl_change_percentage",
                    0.00,
                ),
                "atl_date": ciso8601.parse_datetime(
                    coin_market.get("atl_date", "2024-01-01T00:00:00Z"),
                ),
            }
            if coin_market.get("market_cap", 0.00) > Config.min_mcap.to_int()
            else {}
        )
        for coin_market in coins_market
    ]

    for coin_market in coins_market:
        if coin_market.items().__len__() == 0:
            continue

        coin = await market_coins_controller.get_by_id(
            coin_market.get("id"),
        )

        if coin is None:
            await market_coins_controller.create(**coin_market)
            continue

        await market_coins_controller.update(**coin_market)

    await client.session.close()
    await session.close()
    return None


# async def update_market_data() -> None:
#     client = CoinGeckoV3Client(api_key=CoinGecko.api_key.to_string())
#     session = async_session()
#     market_coins_controller = MarketCoinsController(session)
#     coins_done = False
#     coins_page = 1

#     while not coins_done:
#         coins_market = await client.markets(per_page=250, page=coins_page)
#         coins_market_json: list[dict] = await coins_market.json()

#         for coin_market in coins_market_json:
#             coin_data = {
#                 "id": coin_market.get("id"),
#                 "symbol": coin_market.get("symbol"),
#                 "current_price": coin_market.get(
#                     "current_price",
#                     0.00,
#                 ),
#                 "market_cap": coin_market.get(
#                     "market_cap",
#                     0.00,
#                 ),
#                 "price_change_24h": coin_market.get(
#                     "price_change_24h",
#                     0.00,
#                 ),
#                 "price_change_percentage_24h": coin_market.get(
#                     "price_change_percentage_24h",
#                     0.00,
#                 ),
#                 "market_cap_change_24h": coin_market.get(
#                     "market_cap_change_24h",
#                     0.00,
#                 ),
#                 "market_cap_change_percentage_24h": coin_market.get(
#                     "market_cap_change_percentage_24h",
#                     0.00,
#                 ),
#                 "ath": coin_market.get(
#                     "ath",
#                     0.00,
#                 ),
#                 "ath_change_percentage": coin_market.get(
#                     "ath_change_percentage",
#                     0.00,
#                 ),
#                 "ath_date": ciso8601.parse_datetime(
#                     coin_market.get("ath_date"),
#                 ),
#                 "atl": coin_market.get(
#                     "atl",
#                     0.00,
#                 ),
#                 "atl_change_percentage": coin_market.get(
#                     "atl_change_percentage",
#                     0.00,
#                 ),
#                 "atl_date": ciso8601.parse_datetime(
#                     coin_market.get("atl_date"),
#                 ),
#             }

#             if coin_data.get("market_cap") < Config.min_mcap.to_int():
#                 coins_done = True
#                 break

#             coin = await market_coins_controller.get_by_id(
#                 coin_data.get("id"),
#             )

#             if coin is None:
#                 await market_coins_controller.create(**coin_data)
#                 continue

#             await market_coins_controller.update(**coin_data)

#         coins_page += 1

#     await client.session.close()
#     await session.close()
#     return None
