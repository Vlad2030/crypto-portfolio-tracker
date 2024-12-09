import dataclasses
import os

import dotenv

dotenv.load_dotenv()
env_path = dotenv.find_dotenv()


@dataclasses.dataclass
class Base:
    name: str
    value: str | None

    @classmethod
    def from_env(cls, key: str) -> "Base":
        return cls(name=key, value=os.getenv(key))

    @classmethod
    def __log_repr__(cls, log_class) -> None:
        for item_name, item_data in cls.__dict__.items():
            log = f"{cls.__name__}.{item_name} {item_data.__class__}"
            if item_name.startswith("_"):
                continue
            if isinstance(item_data, classmethod):
                log += f": {item_data.__func__(cls).__str__()}"
                log_class.info(log)
                continue
            log += f" ({item_data.name}): {item_data.value}"
            log_class.info(log)

    def update(self, value: str | None) -> None:
        self.value = value

    def update_env(self, value: str | None) -> None:
        dotenv.set_key(env_path, self.name, value)
        self.update(value)

    def to_string(self) -> str:
        return str(self.value)

    def to_int(self) -> int:
        return int(self.value)

    def to_float(self) -> int:
        return self.to_int().__float__()

    def to_bool(self) -> bool:
        return True if self.to_string().lower() == "true" else False

    def to_list[T](self, sep: str = ",") -> list[T]:
        return [T(item) for item in self.value.split(sep)]


@dataclasses.dataclass
class Database(Base):
    path = Base.from_env("DATABASE_PATH")

    @classmethod
    def url(cls) -> str:
        return f"sqlite+aiosqlite:///./{cls.path.to_string()}"


@dataclasses.dataclass
class Config(Base):
    portfolio_id = Base.from_env("CONFIG_PORTFOLIO_ID")
    currency = Base.from_env("CONFIG_CURRENCY")
    buy_amount = Base.from_env("CONFIG_BUY_AMOUNT")
    min_mcap = Base.from_env("CONFIG_MIN_MCAP")
    market_data_update_interval = Base.from_env(
        "CONFIG_MARKET_DATA_UPDATE_INTERVAL"
    )
    telegram_message_update_interval = Base.from_env(
        "CONFIG_TELEGRAM_MESSAGE_UPDATE_INTERVAL"
    )


@dataclasses.dataclass
class Telegram(Base):
    bot_token = Base.from_env("TELEGRAM_BOT_TOKEN")
    channel_id = Base.from_env("TELEGRAM_CHANNEL_ID")
    channel_message_id = Base.from_env("TELEGRAM_CHANNEL_MESSAGE_ID")


@dataclasses.dataclass
class CoinGecko(Base):
    api_key = Base.from_env("COINGECKO_API_KEY")
