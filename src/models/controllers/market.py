import datetime

import sqlalchemy
from sqlalchemy import desc, insert, select, update, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from models.controllers.base import BaseController
from models.market import MarketCoinsDatabase


class MarketCoinsController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_all(self) -> list[MarketCoinsDatabase]:
        query = select(MarketCoinsDatabase).order_by(
            desc(MarketCoinsDatabase.market_cap)
        )
        result = await self.custom_query(query)

        return result.scalars().all()

    async def get_by_id(self, id: str) -> MarketCoinsDatabase | None:
        query = select(MarketCoinsDatabase).where(MarketCoinsDatabase.id == id)
        result = await self.custom_query(query)

        return result.scalars().one_or_none()

    async def create(
        self,
        id: str,
        symbol: str,
        current_price: float,
        market_cap: int,
        price_change_24h: float,
        price_change_percentage_24h: float,
        market_cap_change_24h: int,
        market_cap_change_percentage_24h: float,
        ath: float,
        ath_change_percentage: float,
        ath_date: datetime.datetime,
        atl: float,
        atl_change_percentage: float,
        atl_date: datetime.datetime,
    ) -> str:
        query = (
            insert(MarketCoinsDatabase)
            .values(
                id=id,
                symbol=symbol,
                current_price=current_price,
                market_cap=market_cap,
                price_change_24h=price_change_24h,
                price_change_percentage_24h=price_change_percentage_24h,
                market_cap_change_24h=market_cap_change_24h,
                market_cap_change_percentage_24h=market_cap_change_percentage_24h,
                ath=ath,
                ath_change_percentage=ath_change_percentage,
                ath_date=ath_date,
                atl=atl,
                atl_change_percentage=atl_change_percentage,
                atl_date=atl_date,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            .returning(MarketCoinsDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def update(
        self,
        id: str,
        symbol: str | None = None,
        current_price: float | None = None,
        market_cap: int | None = None,
        price_change_24h: float | None = None,
        price_change_percentage_24h: float | None = None,
        market_cap_change_24h: int | None = None,
        market_cap_change_percentage_24h: float | None = None,
        ath: float | None = None,
        ath_change_percentage: float | None = None,
        ath_date: datetime.datetime | None = None,
        atl: float | None = None,
        atl_change_percentage: float | None = None,
        atl_date: datetime.datetime | None = None,
    ) -> MarketCoinsDatabase:
        values: dict = {"updated_at": datetime.datetime.now()}

        if symbol is not None:
            values["symbol"] = symbol

        if current_price is not None:
            values["current_price"] = current_price

        if market_cap is not None:
            values["market_cap"] = market_cap

        if price_change_24h is not None:
            values["price_change_24h"] = price_change_24h

        if price_change_percentage_24h is not None:
            values["price_change_percentage_24h"] = price_change_percentage_24h

        if market_cap_change_24h is not None:
            values["market_cap_change_24h"] = market_cap_change_24h

        if market_cap_change_percentage_24h is not None:
            values["market_cap_change_percentage_24h"] = (
                market_cap_change_percentage_24h
            )

        if ath is not None:
            values["ath"] = ath

        if ath_change_percentage is not None:
            values["ath_change_percentage"] = ath_change_percentage

        if ath_date is not None:
            values["ath_date"] = ath_date

        if atl is not None:
            values["atl"] = atl

        if atl_change_percentage is not None:
            values["atl_change_percentage"] = atl_change_percentage

        if atl_date is not None:
            values["atl_date"] = atl_date

        query = (
            update(MarketCoinsDatabase)
            .where(MarketCoinsDatabase.id == id)
            .values(**values)
            .returning(MarketCoinsDatabase)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()
