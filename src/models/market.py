import datetime
import uuid

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import column_property, mapped_column, relationship

from core.database import Base


class MarketCoinsDatabase(Base):
    __tablename__ = "market_coins"

    id = mapped_column(String, primary_key=True, unique=True)
    symbol = mapped_column(String, nullable=False)
    current_price = mapped_column(Float, nullable=False)
    market_cap = mapped_column(Integer, nullable=False)
    price_change_24h = mapped_column(Float, nullable=True)
    price_change_percentage_24h = mapped_column(Float, nullable=True)
    market_cap_change_24h = mapped_column(Integer, nullable=True)
    market_cap_change_percentage_24h = mapped_column(Float, nullable=True)
    ath = mapped_column(Float, nullable=False)
    ath_change_percentage = mapped_column(Float, nullable=False)
    ath_date = mapped_column(DateTime, nullable=False)
    atl = mapped_column(Float, nullable=False)
    atl_change_percentage = mapped_column(Float, nullable=False)
    atl_date = mapped_column(DateTime, nullable=False)
    created_at = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
    )
    updated_at = mapped_column(
        DateTime,
        nullable=False,
        onupdate=datetime.datetime.now,
    )
