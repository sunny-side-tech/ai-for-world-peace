from world_peace.stats import PortfolioStatistics
from world_peace.model import Portfolio, Position
from pytest import fixture
from decimal import Decimal


@fixture
def profitable_position() -> Position:
    return Position(
        asset="AAPL",
        rate_of_return=2.0
    )


@fixture
def single_asset_portfolio(profitable_position) -> Portfolio:
    return Portfolio(
        positions=[profitable_position]
    )


def test_single_asset_portfolio(single_asset_portfolio) -> None:
    portfolio_statistics = PortfolioStatistics(portfolio=single_asset_portfolio)

    assert portfolio_statistics.compound_annual_growth_rate() == 1.0
    assert portfolio_statistics.sharp_ratio() == Decimal("0.71")
