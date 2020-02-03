import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--account", type=click.Choice(['cash', 'margin', 'futures']), default="cash")
@click.option("--order-id", type=str, required=True, help="order id (provided by server when placing order) to cancel")
@click.option("--symbol", type=str, required=True)
@click.option("--resp-inst", type=click.Choice(['ACK', 'ACCEPT', 'DONE']), default="ACCEPT")
@click.option('--verbose/--no-verbose', default=False)
def run(config, account, order_id, symbol, resp_inst, verbose):
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    url = f"{host}/{group}/api/pro/futures/order"
    ts = utc_timestamp()
    order = dict(
        id = uuid32(),
        orderId = order_id,
        time = ts,
        symbol = symbol,
        respInst = resp_inst,
    )

    if verbose:
        print(f"url: {url}")
        print(f"order: {order}")
    headers = make_auth_headers(ts, "order", apikey, secret)
    res = requests.delete(url, headers=headers, json=order)

    pprint(parse_response(res))


if __name__ == "__main__":
    run()
