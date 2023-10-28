from decimal import Decimal
from world_peace.model import Portfolio
from statistics import mean, stdev


class PortfolioStatistics:
    # per time slice

    risk_free_rate: Decimal = Decimal(0.0)
    portfolio: Portfolio

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    # TODO
    def compound_annual_growth_rate(self):
        average_returns = mean([a.rate_of_return for a in self.portfolio.positions])
        return average_returns

    def sharp_ratio(self):
        portfolio_returns = [a.rate_of_return for a in self.portfolio.positions]
        portfolio_std = stdev(portfolio_returns)
        sharp_ratio = (self.compound_annual_growth_rate() - self.risk_free_rate) / portfolio_std
        return round(sharp_ratio, 2)

    def calmar_ratio(self, *args, **kwargs):
        raise NotImplementedError()

    def maximum_drawdown(self, *args, **kwargs):
        raise NotImplementedError()

    def maximum_drawdown_duration(self, *args, **kwargs):
        raise NotImplementedError()
