from decimal import Decimal
from world_peace.model import Portfolio, DrawDown
from statistics import mean, stdev
from pydantic import BaseModel


class PortfolioStatistics:
    # per time slice

    risk_free_rate: Decimal = Decimal(0.0)
    portfolio: Portfolio
    hp: dict[int, Portfolio]

    def __init__(self, portfolio: Portfolio, hp: dict):
        self.portfolio = portfolio
        self.historical_portfolios = hp

    # TODO
    def compound_annual_growth_rate(self):
        current_value = sum(a.market_value for a in self.portfolio.positions)
        starting_value = self.historical_portfolios[0].total_market_value
        print(current_value / starting_value, self.historical_portfolios)
        print("time_idx", self.portfolio.time_idx)
        cagr = ((current_value / starting_value) ** (Decimal(1) / Decimal(self.portfolio.time_idx)) - 1)
        return cagr

    def sharp_ratio(self):
        historical_returns = []
        for k, v in self.historical_portfolios.items():
            for p in v.positions:
                historical_returns.append(p.rate_of_return)

        portfolio_returns = [a.rate_of_return for a in self.portfolio.positions] + historical_returns
        portfolio_std = stdev(portfolio_returns)
        sharp_ratio = (self.compound_annual_growth_rate() - self.risk_free_rate) / portfolio_std
        return round(sharp_ratio, 2)

    def calmar_ratio(self, *args, **kwargs) -> float:
        return self.compound_annual_growth_rate() / self.drawdown().percent

    def drawdown(self, *args, **kwargs) -> DrawDown:
        historical_portfolios: list[Portfolio] = [v for v in self.historical_portfolios.values()]
        best_day: Portfolio = max(historical_portfolios, key=lambda p: p.total_market_value)
        worst_day: Portfolio = min(historical_portfolios[best_day.time_idx:], key=lambda p: p.total_market_value)
        draw_down_percent = (best_day.total_market_value - worst_day.total_market_value) / best_day.total_market_value
        draw_down_duration = abs(worst_day.time_idx - best_day.time_idx)
        # 1. Find Max portfolio, find min portfolio
        # 2.  MDD = (Peak Value - Trough Value) / Peak Value
        # 3. count number of values between peak value and trough value
        print(f"best {best_day} \n worst {worst_day}"
              f""
              f"pct: {draw_down_percent} dur: {draw_down_duration}")
        return DrawDown(
            time_idx=worst_day.time_idx,
            percent=draw_down_percent,
            duration=draw_down_duration
        )
