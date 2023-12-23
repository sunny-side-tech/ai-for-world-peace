from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class Position(BaseModel):
    # TOD add history reference
    asset: str
    rate_of_return: Decimal
    start_idx: int = 0
    market_value: Decimal
    notional: int

    def from_cash(self, amount: Decimal) -> "Position":
        # without trading anything our cash has 0 returns
        # this position marks the initial portfolio state upon instantiation
        return Position(
            asset="CASH",
            rate_of_return=0.0,
            start_idx=0,
            notional=amount,
            market_value=amount,
            time_idx=0,
        )


class Portfolio(BaseModel):
    positions: list[Position]
    time: datetime = datetime.now()
    time_idx: int

    @property
    def total_market_value(self):
        return sum([p.market_value for p in self.positions])


class DrawDown(BaseModel):
    time_idx: int
    percent: Decimal
    duration: int
