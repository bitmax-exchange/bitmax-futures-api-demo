import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--order-id", type=str, required=True, help="order id")
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option('--verbose/--no-verbose', default=False)
def run(order_id, config, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    group = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{group}/api/pro/v1/futures/order/status"
    params = dict(orderId = order_id)

    if verbose:
        print(f"url: {url}")
        print(f"params: {params}")

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "order/status", apikey, secret)
    res = requests.get(url, headers=headers, params=params)

    pprint(parse_response(res))



if __name__ == "__main__":
    run()
