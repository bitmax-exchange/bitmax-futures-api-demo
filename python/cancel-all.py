import os 
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--account", type=click.Choice(['cash', 'margin', 'futures']), default="futures")
@click.option("--symbol", type=str, default=None, help="if not provided, cancel all orders.")
@click.option("--config", type=str, default="config.json", help="path to the config file")
@click.option('--verbose/--no-verbose', default=False)
def run(account, symbol, config, verbose):

    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    group = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    method = "order/all"

    url = f"{host}/{group}/api/pro/v1/{account}/order/all"

    params = dict(symbol = symbol)

    if verbose:
        print(f"User url: {url}")
        print(f"User params: {params}")

    ts = utc_timestamp()
    headers = make_auth_headers(ts, method, apikey, secret)

    res = requests.delete(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
