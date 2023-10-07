from polygon.stocks import StocksClient
from config import ServiceConfig


config = ServiceConfig()

client = StocksClient(api_key=config.api_key)

aggy_daddy = client.get_aggregate_bars(symbol="AAPL", multiplier=1, timespan="minute",
                                       from_date="2023-01-01", to_date="2023-06-13", raw_response=False, limit=50000)

# TODO do math
