from world_peace.stats import compound_annual_growth_rate


def test_cagr():
    returns = 1.0
    periods = 252
    cagr_returns = 1127

    assert cagr_returns == compound_annual_growth_rate(returns, periods)


