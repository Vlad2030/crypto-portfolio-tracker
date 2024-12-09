import datetime
import uuid

import sqlalchemy
from sqlalchemy import asc, desc, insert, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from models.controllers.base import BaseController
from models.portfolio import PortfolioCoinsDatabase, PortfolioDatabase


class PortfolioController(BaseController):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_all(self) -> list[PortfolioDatabase]:
        query = select(PortfolioDatabase).options(
            subqueryload(PortfolioDatabase.coins)
        )
        result = await self.custom_query(query)

        return result.scalars().all()

    async def get_by_id(self, id: uuid.UUID) -> PortfolioDatabase | None:
        query = (
            select(PortfolioDatabase)
            .options(subqueryload(PortfolioDatabase.coins))
            .where(PortfolioDatabase.id == id)
        )
        result = await self.custom_query(query)

        return result.scalars().one_or_none()

    async def create(self) -> str:
        query = (
            insert(PortfolioDatabase)
            .values(
                id=str(uuid.uuid4()),
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            .returning(PortfolioDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def update(
        self,
        id: uuid.UUID,
        quote_value: float | None = None,
        quote_value_ath: float | None = None,
        quote_value_atl: float | None = None,
        quote_value_invested: float | None = None,
        pnl_percentage: float | None = None,
        pnl_percentage_ath: float | None = None,
        pnl_percentage_atl: float | None = None,
        pnl_quote_value: float | None = None,
        pnl_quote_value_ath: float | None = None,
        pnl_quote_value_atl: float | None = None,
    ) -> str:
        values: dict = {"updated_at": datetime.datetime.now()}

        if quote_value is not None:
            values["quote_value"] = quote_value

        if quote_value_ath is not None:
            values["quote_value_ath"] = quote_value_ath

        if quote_value_atl is not None:
            values["quote_value_atl"] = quote_value_atl

        if quote_value_invested is not None:
            values["quote_value_invested"] = quote_value_invested

        if pnl_percentage is not None:
            values["pnl_percentage"] = pnl_percentage

        if pnl_percentage_ath is not None:
            values["pnl_percentage_ath"] = pnl_percentage_ath

        if pnl_percentage_atl is not None:
            values["pnl_percentage_atl"] = pnl_percentage_atl

        if pnl_quote_value is not None:
            values["pnl_quote_value"] = pnl_quote_value

        if pnl_quote_value_ath is not None:
            values["pnl_quote_value_ath"] = pnl_quote_value_ath

        if pnl_quote_value_atl is not None:
            values["pnl_quote_value_atl"] = pnl_quote_value_atl

        query = (
            update(PortfolioDatabase)
            .where(PortfolioDatabase.id == id)
            .values(**values)
            .returning(PortfolioDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def get_coins(self) -> PortfolioCoinsDatabase | None:
        query = select(PortfolioCoinsDatabase)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_coin_by_id(
        self,
        id: uuid.UUID,
    ) -> PortfolioCoinsDatabase | None:
        query = select(PortfolioCoinsDatabase).where(
            PortfolioCoinsDatabase.id == id
        )
        result = await self.custom_query(query)

        return result.scalars().one_or_none()

    async def get_coin_by_coin_id(
        self,
        portfolio_id: uuid.UUID,
        coin_id: str,
    ) -> PortfolioCoinsDatabase | None:
        query = (
            select(PortfolioCoinsDatabase)
            .where(PortfolioCoinsDatabase.coin_id == coin_id)
            .where(PortfolioCoinsDatabase.portfolio_id == portfolio_id)
        )
        result = await self.custom_query(query)

        return result.scalars().one_or_none()

    async def get_coin_gainers(
        self,
        portfolio_id: uuid.UUID,
        limit: int = 10,
    ) -> list[PortfolioCoinsDatabase]:
        query = (
            select(PortfolioCoinsDatabase)
            .where(
                PortfolioCoinsDatabase.portfolio_id == portfolio_id,
            )
            .order_by(desc(PortfolioCoinsDatabase.quote_value))
            .limit(limit)
        )
        result = await self.custom_query(query)

        return sorted(
            result.scalars().all(),
            key=(lambda k: k.quote_value),
            reverse=True,
        )

    async def get_coin_losers(
        self,
        portfolio_id: uuid.UUID,
        limit: int = 10,
    ) -> list[PortfolioCoinsDatabase]:
        query = (
            select(PortfolioCoinsDatabase)
            .where(
                and_(
                    PortfolioCoinsDatabase.portfolio_id == portfolio_id,
                    PortfolioCoinsDatabase.pnl_percentage > -99,
                )
            )
            .order_by(asc(PortfolioCoinsDatabase.quote_value))
            .limit(limit)
        )
        result = await self.custom_query(query)

        return sorted(
            result.scalars().all(),
            key=(lambda k: k.quote_value),
            reverse=False,
        )

    async def create_coin(
        self,
        portfolio_id: uuid.UUID,
        coin_id: str,
        quantity: int | float,
        quote_value: int | float,
    ) -> str:
        query = (
            insert(PortfolioCoinsDatabase)
            .values(
                id=str(uuid.uuid4()),
                portfolio_id=portfolio_id,
                coin_id=coin_id,
                quantity=quantity,
                quantity_ath=quantity,
                quantity_atl=quantity,
                quote_value=quote_value,
                quote_value_ath=quote_value,
                quote_value_atl=quote_value,
                quote_value_invested=quote_value,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            .returning(PortfolioCoinsDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def create_coins(
        self,
        portfolio_id: uuid.UUID,
        coins: list[dict],
    ) -> list[str]:
        query = (
            insert(PortfolioCoinsDatabase)
            .values(coins)
            .returning(PortfolioCoinsDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def update_coin(
        self,
        id: uuid.UUID,
        quantity: float | None = None,
        quantity_ath: float | None = None,
        quantity_atl: float | None = None,
        quote_value: float | None = None,
        quote_value_ath: float | None = None,
        quote_value_atl: float | None = None,
        quote_value_invested: float | None = None,
        pnl_percentage: float | None = None,
        pnl_percentage_ath: float | None = None,
        pnl_percentage_atl: float | None = None,
        pnl_quote_value: float | None = None,
        pnl_quote_value_ath: float | None = None,
        pnl_quote_value_atl: float | None = None,
    ) -> str:
        values: dict = {"updated_at": datetime.datetime.now()}

        if quantity is not None:
            values["quantity"] = quantity

        if quantity_ath is not None:
            values["quantity_ath"] = quantity_ath

        if quantity_atl is not None:
            values["quantity_atl"] = quantity_atl

        if quote_value is not None:
            values["quote_value"] = quote_value

        if quote_value_ath is not None:
            values["quote_value_ath"] = quote_value_ath

        if quote_value_atl is not None:
            values["quote_value_atl"] = quote_value_atl

        if quote_value_invested is not None:
            values["quote_value_invested"] = quote_value_invested

        if pnl_percentage is not None:
            values["pnl_percentage"] = pnl_percentage

        if pnl_percentage_ath is not None:
            values["pnl_percentage_ath"] = pnl_percentage_ath

        if pnl_percentage_atl is not None:
            values["pnl_percentage_atl"] = pnl_percentage_atl

        if pnl_quote_value is not None:
            values["pnl_quote_value"] = pnl_quote_value

        if pnl_quote_value_ath is not None:
            values["pnl_quote_value_ath"] = pnl_quote_value_ath

        if pnl_quote_value_atl is not None:
            values["pnl_quote_value_atl"] = pnl_quote_value_atl

        query = (
            update(PortfolioCoinsDatabase)
            .where(PortfolioCoinsDatabase.id == id)
            .values(**values)
            .returning(PortfolioCoinsDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().first()

    async def update_coins(
        self,
        portfolio_id: uuid.UUID,
        coins: list[dict],
    ) -> list[str]:
        query = (
            update(PortfolioCoinsDatabase)
            .where(PortfolioCoinsDatabase.portfolio_id == portfolio_id)
            .values(coins)
            .returning(PortfolioCoinsDatabase.id)
        )
        result = await self.custom_query(query)

        await self.session.commit()

        return result.scalars().all()
