import asyncio
import time

import aiocron
from loguru import logger

from core import data, database, telegram
from tasks import coins, portfolio, telegram
from utils import crontab, tasks

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@aiocron.crontab(
    spec=crontab.generate_expression(
        interval_seconds=data.Config.market_data_update_interval.to_int(),
    ),
    loop=loop,
)
@tasks.log
async def update_market_data_task() -> None:
    return await coins.update_market_data()


@aiocron.crontab(
    spec=crontab.generate_expression(
        interval_seconds=data.Config.telegram_message_update_interval.to_int(),
    ),
    loop=loop,
)
@tasks.log
async def update_channel_message_task() -> None:
    return await telegram.update_channel_message()


@aiocron.crontab(
    spec=crontab.generate_expression(
        interval_seconds=data.Config.market_data_update_interval.to_int()
    ),
    loop=loop,
)
@tasks.log
async def update_portfolio_stats_task() -> None:
    return await portfolio.update_stats()


async def main() -> None:
    logger.info("Created by lalka2003")

    database_session = database.async_session()
    database_connection = database_session.is_active
    await database_session.close()
    logger.info(f"Database connected: {database_connection}")

    telegram_channel = await telegram.bot.get_chat(
        chat_id=data.Telegram.channel_id.to_int(),
    )
    logger.info(f"Telegram channel: @{telegram_channel.username}")

    data.Config.__log_repr__(logger)
    data.CoinGecko.__log_repr__(logger)
    data.Database.__log_repr__(logger)
    data.Telegram.__log_repr__(logger)

    logger.info("Tracker started")

    while True:
        await asyncio.sleep(1.00)


if __name__ == "__main__":
    loop.run_until_complete(main())
