from pandas import DataFrame, read_csv, concat
from polygon.stocks import StocksClient
from world_peace.config import ServiceConfig


# untested scratch I wrote while drunk, can be ignored

config = ServiceConfig()
client = StocksClient(api_key=config.polygon_api_key)

aggy_daddy = client.get_aggregate_bars(
    symbol="AAPL",
    multiplier=1,
    timespan="minute",
    from_date="2023-01-01",
    to_date="2023-06-13",
    raw_response=False,
    limit=50000,
)


def get_close_by_date(ticker: str) -> DataFrame:
    data = read_csv(f"./data/{ticker}.csv")[["Adj Close", "Date"]]
    data.index = data.pop("Date")
    data["Ticker"] = ticker
    return data


ticker_allocation = [("AAPL", 0.35), ("CSCO", 0.25), ("IBM", 0.2), ("AMZN", 0.2)]

bar_list = [get_close_by_date(b[0]) for b in ticker_allocation]


def get_positions(bar_list: list[DataFrame], initial_size: int) -> list[DataFrame]:
    for df in bar_list:
        df["Norm Return"] = df["Adj Close"] / df.iloc[0]["Adj Close"]

    allocations: list[float] = [a[1] for a in ticker_allocation]
    for df, allocation in zip(bar_list, allocations):
        df["Allocation"] = df["Norm Return"] * allocation

    for df in bar_list:
        df[f"{df['Ticker'].iloc[0]} Position"] = df["Allocation"] * initial_size

    return bar_list


positions = get_positions(bar_list, 10000)


def get_portfolio(positions: list[DataFrame]) -> DataFrame:
    all_positions = [p[f"{p['Ticker'].iloc[0]} Position"] for p in positions]
    portfolio = concat(all_positions, axis=1)
    portfolio["Total Pos"] = portfolio.sum(axis=1)
    return portfolio


portfolio = get_portfolio(positions)


def get_daily_returns(portfolio: DataFrame) -> DataFrame:
    portfolio["Daily Return"] = portfolio["Total Pos"].pct_change(1)
    return portfolio


returns = get_daily_returns(portfolio)


def get_sharp_ratio(returns: DataFrame) -> DataFrame:
    sharp_ratio = returns["Daily Return"].mean() / portfolio["Daily Return"].std()
    return sharp_ratio


def get_annualized_sharp_ratio(returns: DataFrame) -> DataFrame:
    sharp_ratio = returns["Daily Return"].mean() / portfolio["Daily Return"].std()
    return (252**0.5) * sharp_ratio


print(get_sharp_ratio(returns))
print(get_annualized_sharp_ratio(returns))
