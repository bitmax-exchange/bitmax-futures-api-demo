import os
import click
import requests
from pprint import pprint

# Local imports
from util import *

@click.command()
@click.option("--account", type=click.Choice(['cash', 'margin', 'futures']), default=None)
@click.option("--symbol", type=str, default=None)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=10)
@click.option("--start-time", type=int, default=0)
@click.option("--end-time", type=int, default=utc_timestamp())
@click.option("--order-type", type=str, default=None)  # "market" or "limit"
@click.option("--side", type=click.Choice(['buy', 'sell']), default=None)
@click.option("--status", type=click.Choice(['Filled', 'Canceled', 'Rejected', 'WithFill']), default=None)
@click.option("--config", type=str, default="config.json", help="path to the config file")
@click.option("--verbose/--no-verbose", default=False)
def run(account, symbol, page, page_size, start_time, end_time, order_type, side, status, config, verbose):

    btmx_cfg = load_config(get_config_or_default(config))['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    url = f"{host}/{group}/api/pro/v1/order/hist"
    ts = utc_timestamp()

    headers = make_auth_headers(ts, "order/hist", apikey, secret)
    params = dict(
        symbol = symbol,
        category = account,
        orderType = order_type,
        page = page,
        pageSize = page_size,
        side = side,
        startTime = start_time,
        endTime = end_time,
        status = status,
    )

    if verbose: 
        print(f"url = {url}")
        print(f"params = {params}")

    res = requests.get(url, params=params, headers=headers)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
