from core.data import Config
from core.database import async_session
from models.controllers.market import MarketCoinsController
from models.controllers.portfolio import PortfolioController


async def update_stats() -> None:
    session = async_session()
    market_coins_controller = MarketCoinsController(session)
    portfolio_controller = PortfolioController(session)

    portfolios = await portfolio_controller.get_all()

    for portfolio in portfolios:
        portfolio_quote_value = 0.00

        for portfolio_coin in portfolio.coins:
            market_coin = await market_coins_controller.get_by_id(
                portfolio_coin.coin_id
            )

            if market_coin is None:
                continue

            portfolio_coin_quote_value = (
                portfolio_coin.quantity * market_coin.current_price
            )
            portfolio_coin_quote_value_ath = (
                portfolio_coin_quote_value
                if portfolio_coin_quote_value > portfolio_coin.quote_value_ath
                else portfolio_coin.quote_value_ath
            )
            portfolio_coin_quote_value_atl = (
                portfolio_coin_quote_value
                if portfolio_coin_quote_value < portfolio_coin.quote_value_atl
                else portfolio_coin.quote_value_atl
            )
            portfolio_coin_pnl_percentage = max(
                (
                    (
                        (
                            portfolio_coin_quote_value
                            - portfolio_coin.quote_value_invested
                        )
                        / portfolio_coin.quote_value_invested
                    )
                    * 100
                ),
                -99.9999,
            )
            portfolio_coin_pnl_percentage_ath = (
                portfolio_coin_pnl_percentage
                if portfolio_coin_pnl_percentage
                > portfolio_coin.pnl_percentage_ath
                else portfolio_coin.pnl_percentage_ath
            )
            portfolio_coin_pnl_percentage_atl = (
                portfolio_coin_pnl_percentage
                if portfolio_coin_pnl_percentage
                < portfolio_coin.pnl_percentage_atl
                else portfolio_coin.pnl_percentage_atl
            )
            portfolio_coin_pnl_quote_value = (
                portfolio_coin_quote_value
                - portfolio_coin.quote_value_invested
            )
            portfolio_coin_pnl_quote_value_ath = (
                portfolio_coin_pnl_quote_value
                if portfolio_coin_pnl_quote_value
                > portfolio_coin.pnl_quote_value_ath
                else portfolio_coin.pnl_quote_value_ath
            )
            portfolio_coin_pnl_quote_value_atl = (
                portfolio_coin_pnl_quote_value
                if portfolio_coin_pnl_quote_value
                < portfolio_coin.pnl_quote_value_atl
                else portfolio_coin.pnl_quote_value_atl
            )

            portfolio_quote_value += portfolio_coin_quote_value

            await portfolio_controller.update_coin(
                id=portfolio_coin.id,
                quote_value=portfolio_coin_quote_value,
                quote_value_ath=portfolio_coin_quote_value_ath,
                quote_value_atl=portfolio_coin_quote_value_atl,
                pnl_percentage=portfolio_coin_pnl_percentage,
                pnl_percentage_ath=portfolio_coin_pnl_percentage_ath,
                pnl_percentage_atl=portfolio_coin_pnl_percentage_atl,
                pnl_quote_value=portfolio_coin_pnl_quote_value,
                pnl_quote_value_ath=portfolio_coin_pnl_quote_value_ath,
                pnl_quote_value_atl=portfolio_coin_pnl_quote_value_atl,
            )

        portfolio_quote_value_ath = (
            portfolio_quote_value
            if portfolio_quote_value > portfolio.quote_value_ath
            else portfolio.quote_value_ath
        )
        portfolio_quote_value_atl = (
            portfolio_quote_value
            if portfolio_quote_value < portfolio.quote_value_atl
            else portfolio.quote_value_atl
        )
        portfolio_pnl_percentage = max(
            (
                (
                    (portfolio_quote_value - portfolio.quote_value_invested)
                    / portfolio.quote_value_invested
                )
                * 100
            ),
            -99.9999,
        )
        portfolio_pnl_percentage_ath = (
            portfolio_pnl_percentage
            if portfolio_pnl_percentage > portfolio.pnl_percentage_ath
            else portfolio.pnl_percentage_ath
        )
        portfolio_pnl_percentage_atl = (
            portfolio_pnl_percentage
            if portfolio_pnl_percentage < portfolio.pnl_percentage_atl
            else portfolio.pnl_percentage_atl
        )
        portfolio_pnl_quote_value = (
            portfolio_quote_value - portfolio.quote_value_invested
        )
        portfolio_pnl_quote_value_ath = (
            portfolio_pnl_quote_value
            if portfolio_pnl_quote_value > portfolio.pnl_quote_value_ath
            else portfolio.pnl_quote_value_ath
        )
        portfolio_pnl_quote_value_atl = (
            portfolio_pnl_quote_value
            if portfolio_pnl_quote_value < portfolio.pnl_quote_value_atl
            else portfolio.pnl_quote_value_atl
        )

        await portfolio_controller.update(
            id=portfolio.id,
            quote_value=portfolio_quote_value,
            quote_value_ath=portfolio_quote_value_ath,
            quote_value_atl=portfolio_quote_value_atl,
            pnl_percentage=portfolio_pnl_percentage,
            pnl_percentage_ath=portfolio_pnl_percentage_ath,
            pnl_percentage_atl=portfolio_pnl_percentage_atl,
            pnl_quote_value=portfolio_pnl_quote_value,
            pnl_quote_value_ath=portfolio_pnl_quote_value_ath,
            pnl_quote_value_atl=portfolio_pnl_quote_value_atl,
        )

    await session.close()

    return None


async def add_new_coins() -> None:
    session = async_session()
    market_coins_controller = MarketCoinsController(session)
    portfolio_controller = PortfolioController(session)

    portfolios = await portfolio_controller.get_all()
    market_coins = await market_coins_controller.get_all()
    market_coins_ids = [market_coin.id for market_coin in market_coins]

    for portfolio in portfolios:
        portfolio_quote_value = portfolio.quote_value
        portfolio_quote_value_invested = portfolio.quote_value_invested
        porfolio_coins_ids = [
            portfolio_coin.coin_id for portfolio_coin in portfolio.coins
        ]

        for market_coins_id in market_coins_ids:
            if market_coins_id not in porfolio_coins_ids:
                market_coin = await market_coins_controller.get_by_id(
                    market_coins_id,
                )

                if market_coin is None:
                    continue

                market_coin_quantity = (
                    Config.buy_amount.to_float() / market_coin.current_price
                )
                market_coin_quote_value = (
                    market_coin_quantity * market_coin.current_price
                )

                await portfolio_controller.create_coin(
                    portfolio_id=portfolio.id,
                    coin_id=market_coin.id,
                    quantity=market_coin_quantity,
                    quote_value=market_coin_quote_value,
                )

                portfolio_quote_value += market_coin_quote_value
                portfolio_quote_value_invested += market_coin_quote_value

        await portfolio_controller.update(
            id=portfolio.id,
            quote_value=portfolio_quote_value,
            quote_value_invested=portfolio_quote_value_invested,
        )

    await session.close()
    return None
