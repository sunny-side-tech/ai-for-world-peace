from pydantic import BaseModel
from decimal import Decimal


class Position(BaseModel):
    asset: str
    rate_of_return: Decimal

    @classmethod
    def starting_point(cls) -> "Position":
        # without trading anything our cash has 0 returns
        # this position marks the initial portfolio state upon instantiation
        return Position(
            asset="CASH",
            rate_of_return=0.0
        )


class Portfolio(BaseModel):
    positions: list[Position]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.positions.insert(0, Position.starting_point())
