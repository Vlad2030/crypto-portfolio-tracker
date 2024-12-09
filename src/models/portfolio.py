import datetime
import uuid

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import column_property, mapped_column, relationship

from core.database import Base

# stupid solution for sqlalchemy.exc.NoReferencedTableError
from models.market import MarketCoinsDatabase


class PortfolioDatabase(Base):
    __tablename__ = "portfolio"

    id = mapped_column(
        String,
        primary_key=True,
        unique=True,
        nullable=False,
        default=str(uuid.uuid4()),
    )
    quote_value = mapped_column(Float, nullable=False, default=0.00)
    quote_value_ath = mapped_column(Float, nullable=False, default=0.00)
    quote_value_atl = mapped_column(Float, nullable=False, default=0.00)
    quote_value_invested = mapped_column(Float, nullable=False, default=0.00)
    pnl_percentage = mapped_column(Float, nullable=True, default=0.00)
    pnl_percentage_ath = mapped_column(Float, nullable=True, default=0.00)
    pnl_percentage_atl = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value_ath = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value_atl = mapped_column(Float, nullable=True, default=0.00)
    created_at = mapped_column(
        DateTime, nullable=False, default=datetime.datetime.now
    )
    updated_at = mapped_column(
        DateTime,
        nullable=False,
        onupdate=datetime.datetime.now,
    )

    coins = relationship(
        "PortfolioCoinsDatabase",
        back_populates="portfolio",
        cascade="all, delete-orphan",
    )


class PortfolioCoinsDatabase(Base):
    __tablename__ = "portfolio_coins"

    id = mapped_column(
        String,
        primary_key=True,
        unique=True,
        nullable=False,
        default=str(uuid.uuid4()),
    )
    portfolio_id = mapped_column(
        String,
        ForeignKey("portfolio.id"),
        nullable=False,
        index=True,
    )
    coin_id = mapped_column(
        String,
        ForeignKey("market_coins.id"),
        nullable=False,
        index=True,
    )
    quantity = mapped_column(Float, nullable=True, default=0.00)
    quantity_ath = mapped_column(Float, nullable=True, default=0.00)
    quantity_atl = mapped_column(Float, nullable=True, default=0.00)
    quote_value = mapped_column(Float, nullable=False, default=0.00)
    quote_value_ath = mapped_column(Float, nullable=False, default=0.00)
    quote_value_atl = mapped_column(Float, nullable=False, default=0.00)
    quote_value_invested = mapped_column(Float, nullable=False, default=0.00)
    pnl_percentage = mapped_column(Float, nullable=True, default=0.00)
    pnl_percentage_ath = mapped_column(Float, nullable=True, default=0.00)
    pnl_percentage_atl = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value_ath = mapped_column(Float, nullable=True, default=0.00)
    pnl_quote_value_atl = mapped_column(Float, nullable=True, default=0.00)
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

    portfolio = relationship("PortfolioDatabase", back_populates="coins")
