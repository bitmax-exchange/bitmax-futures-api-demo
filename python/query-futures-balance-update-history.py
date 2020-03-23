import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=10)
@click.option('--verbose/--no-verbose', default=False)
def run(config, page, page_size, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    grp = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{grp}/api/pro/v1/futures/balance-update-history"

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "futures/balance-update-history", apikey, secret)
    params = dict(page = page, pageSize = page_size)

    if verbose: 
        print(f"url = {url}")
        print(f"params = {params}")

    res = requests.get(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
