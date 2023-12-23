from world_peace.stats import PortfolioStatistics
from world_peace.model import Portfolio, Position
from pytest import fixture
from decimal import Decimal


@fixture
def profitable_position() -> Position:
    return Position(
        asset="AAPL",
        rate_of_return=2.0,
        start_idx=1,
        market_value=200.0,
        notional=1,
    )


@fixture
def single_asset_portfolio(profitable_position: Position) -> Portfolio:
    return Portfolio(
        positions=[profitable_position],
        time_idx=2,
    )


@fixture
def historical_single_asset_portfolios(profitable_position) -> dict[int, Portfolio]:
    cash_start = Position(
        **{
            "rate_of_return": 0.0,
            "start_idx": 0,
            "market_value": 100.0,
            "notional": 100,
            "time_index": 0,
            "asset": "CASH",
        }
    )
    first_position = Position(
        **{
            "rate_of_return": 0.0,
            "start_idx": 1,
            "market_value": 100.0,
            "notional": 1,
            "time_index": 1,
            "asset": "AAPL",
        }
    )

    first_cash_portfolio = Portfolio(positions=[cash_start], time_idx=0)
    first_traded_portfolio = Portfolio(positions=[first_position], time_idx=1)

    return {
        0: first_cash_portfolio,
        1: first_traded_portfolio,
    }


@fixture
def historical_portfolio_with_drawdown(
    historical_single_asset_portfolios,
) -> dict[int, Portfolio]:
    first_position_with_return = Position(
        **{
            "rate_of_return": 1.0,
            "start_idx": 1,
            "market_value": 200.0,
            "notional": 1,
            "time_index": 2,
            "asset": "AAPL",
        }
    )
    first_position_with_drawdown = Position(
        **{
            "rate_of_return": 1.0,
            "start_idx": 1,
            "market_value": 150.0,
            "notional": 1,
            "time_index": 3,
            "asset": "AAPL",
        }
    )

    first_position_increased = Position(
        **{
            "rate_of_return": 1.0,
            "start_idx": 1,
            "market_value": 170.0,
            "notional": 1,
            "time_index": 4,
            "asset": "AAPL",
        }
    )

    first_position_with_return = Portfolio(
        positions=[first_position_with_return], time_idx=2
    )

    first_position_with_drawdown = Portfolio(
        positions=[first_position_with_drawdown], time_idx=3
    )
    first_position_increased = Portfolio(
        positions=[first_position_increased], time_idx=4
    )

    return {
        **historical_single_asset_portfolios,
        2: first_position_with_return,
        3: first_position_with_drawdown,
        4: first_position_increased,
    }


@fixture
def single_asset_statistics(
    single_asset_portfolio, historical_single_asset_portfolios
) -> PortfolioStatistics:
    portfolio_statistics = PortfolioStatistics(
        portfolio=single_asset_portfolio, hp=historical_single_asset_portfolios
    )
    return portfolio_statistics


@fixture
def single_asset_statistics_with_drawdown(
    single_asset_portfolio, historical_portfolio_with_drawdown
) -> PortfolioStatistics:
    stats = PortfolioStatistics(
        portfolio=single_asset_portfolio, hp=historical_portfolio_with_drawdown
    )
    return stats


def test_sharp_ratio__single_asset_portfolio(single_asset_statistics) -> None:
    assert round(single_asset_statistics.compound_annual_growth_rate(), 2) == Decimal(
        ".41"
    )
    # TODO check sharp ratio math
    assert single_asset_statistics.sharp_ratio() == Decimal("0.36")


def test_maximum_drawdown__single_asset_portfolio(
    single_asset_statistics_with_drawdown: PortfolioStatistics,
) -> None:
    drawdown = single_asset_statistics_with_drawdown.drawdown()
    assert round(float(drawdown.percent), 2) == 0.25
    assert drawdown.duration == 1
    assert drawdown.time_idx == 3


def test_calmar_ratio__single_asset_portfolio(
    single_asset_statistics_with_drawdown: PortfolioStatistics,
) -> None:
    drawdown = single_asset_statistics_with_drawdown.drawdown()
    cagr = single_asset_statistics_with_drawdown.compound_annual_growth_rate()
    assert (
        cagr / drawdown.percent == single_asset_statistics_with_drawdown.calmar_ratio()
    )
