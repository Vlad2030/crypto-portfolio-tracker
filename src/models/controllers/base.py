from loguru import logger
import sqlalchemy
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.asyncio import AsyncSession


class BaseController:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def custom_query(
        self,
        query: sqlalchemy.Executable,
        params: list[dict] | dict | None = None,
        execution_options: dict | None = None,
    ) -> sqlalchemy.Result:
        return await self.session.execute(
            statement=query,
            params=params,
            execution_options=execution_options,
        )

    async def custom_logged_query(
        self,
        query: sqlalchemy.Executable,
        params: list[dict] | dict | None = None,
        execution_options: dict | None = None,
        compile_kwargs: dict = {"literal_binds": False},
    ) -> sqlalchemy.Result:
        raw_sql = str(
            query.compile(
                dialect=sqlite.dialect(),
                compile_kwargs=compile_kwargs,
            )
        )
        log_message = f"NEW QUERY: {raw_sql}"
        logger.info(log_message)

        return await self.custom_query(query, params, execution_options)
