from loguru import logger

from core.data import Config, Telegram
from core.database import async_session
from core.telegram import bot, md
from models.controllers.market import MarketCoinsController
from models.controllers.portfolio import PortfolioController
from utils.aiogram import InlineKeyboards


async def update_channel_message() -> None:
    session = async_session()
    market_coins_controller = MarketCoinsController(session)
    portfolio_controller = PortfolioController(session)

    telegram_channel = await bot.get_chat(
        chat_id=Telegram.channel_id.to_string(),
    )
    telegram_channel_post_url = "https://t.me/{username}/{message_id}".format(
        username=telegram_channel.username,
        message_id=Telegram.channel_message_id.to_string(),
    )

    portfolio = await portfolio_controller.get_by_id(
        Config.portfolio_id.to_string(),
    )
    portfolio_coin_gainers = await portfolio_controller.get_coin_gainers(
        portfolio_id=portfolio.id,
        limit=5,
    )
    portfolio_coin_losers = await portfolio_controller.get_coin_losers(
        portfolio_id=portfolio.id,
        limit=5,
    )

    coin_message_template = (
        "\t${symbol} {quote_value:,.2f}$ ({quote_value_pnl:+,.2f}$)"
    )
    gainers_message_text = "\n".join(
        [
            coin_message_template.format(
                symbol=(
                    await market_coins_controller.get_by_id(coin.coin_id)
                ).symbol.upper(),
                quote_value=coin.quote_value,
                quote_value_pnl=(coin.quote_value - coin.quote_value_invested),
            )
            for coin in portfolio_coin_gainers
        ]
    )
    losers_message_text = "\n".join(
        [
            coin_message_template.format(
                symbol=(
                    await market_coins_controller.get_by_id(coin.coin_id)
                ).symbol.upper(),
                quote_value=coin.quote_value,
                quote_value_pnl=(coin.quote_value - coin.quote_value_invested),
            )
            for coin in portfolio_coin_losers
        ]
    )
    message_text = md.hcode(
        f"Balance: {portfolio.quote_value:,.2f}$ ({portfolio.pnl_percentage:+.2f}%)\n\n"
        f"Top {len(portfolio_coin_gainers)} gainers:\n"
        f"{gainers_message_text}\n\n"
        f"Top {len(portfolio_coin_losers)} losers:\n"
        f"{losers_message_text}\n\n"
        f"Total:\n"
        f"\tInvested {portfolio.quote_value_invested:,.2f}$\n"
        f"\tTokens {len(portfolio.coins)}\n"
        f"\tATH profit {portfolio.pnl_quote_value_ath:+,.2f}$ ({portfolio.pnl_percentage_ath:+,.2f}%)\n"
        f"\tATL profit {portfolio.pnl_quote_value_atl:+,.2f}$ ({portfolio.pnl_percentage_atl:+,.2f}%)\n\n"
    )
    message_keyboard = InlineKeyboards.build_keyboard(
        buttons=[
            [
                InlineKeyboards.build_button(
                    text="About the experiment",
                    url=telegram_channel_post_url,
                ),
            ],
        ],
    )

    await session.close()

    try:
        await bot.edit_message_text(
            text=message_text,
            chat_id=Telegram.channel_id.to_int(),
            message_id=Telegram.channel_message_id.to_int(),
            reply_markup=message_keyboard,
        )
    except Exception as e:
        logger.error(e.__repr__())
        pass

    return None
