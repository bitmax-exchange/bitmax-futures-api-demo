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
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    group = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

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
