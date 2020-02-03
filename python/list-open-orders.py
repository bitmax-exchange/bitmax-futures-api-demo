import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option('--verbose/--no-verbose', default=False)
def run(config, verbose):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    url = f"{host}/{group}/api/pro/v1/futures/order/open"

    if verbose:
        print(f"url: {url}")
        print(f"order: {order}")

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "order/open", apikey, secret)
    res = requests.get(url, headers=headers)

    pprint(parse_response(res))



if __name__ == "__main__":
    run()
