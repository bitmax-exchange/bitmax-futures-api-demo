import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--symbol", type=str, default=None, help="symbol filter")
@click.option("--page", type=str, default=None, help="value for the page parameter")
@click.option("--size", type=str, default=None, help="value for the pageSize parameter")
@click.option('--verbose/--no-verbose', default=False)
def run(config, symbol, page, size, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    grp = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{grp}/api/pro/v1/futures/funding-payments"
    params = dict(symbol=symbol, page=page, pageSize=size)

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "futures/funding-payments", apikey, secret)

    if verbose: 
        print(f"url = {url}")
        print(f"params = {params}")

    res = requests.get(url, params=params, headers=headers)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
