import asyncio
import uuid

import dotenv

from src.core.data import Config, Database
from src.core.database import async_create_all, async_session
from src.models.controllers.market import MarketCoinsController
from src.models.controllers.portfolio import PortfolioController
from src.tasks.coins import update_market_data


async def main() -> None:
    await async_create_all()
    await update_market_data()

    session = async_session()
    portfolio_controller = PortfolioController(session)
    market_controller = MarketCoinsController(session)

    portfolio_id = await portfolio_controller.create()
    market_coins = await market_controller.get_all()

    Config.portfolio_id.update_env(portfolio_id)
    total_coin_quote_value = 0.00

    for coin in market_coins:
        coin_portfolio = await portfolio_controller.get_coin_by_coin_id(
            portfolio_id,
            coin.id,
        )

        if coin_portfolio is None:
            coin_quantity = Config.buy_amount.to_float() / coin.current_price
            coin_quote_value = coin.current_price * coin_quantity
            total_coin_quote_value += coin_quote_value

            coin_portfolio_id = await portfolio_controller.create_coin(
                portfolio_id,
                coin.id,
                coin_quantity,
                coin_quote_value,
            )

    await portfolio_controller.update(
        id=portfolio_id,
        quote_value=total_coin_quote_value,
        quote_value_ath=total_coin_quote_value,
        quote_value_atl=0.00,
        quote_value_invested=total_coin_quote_value,
    )

    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
