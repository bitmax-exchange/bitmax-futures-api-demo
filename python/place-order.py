import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *



@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--symbol", type=str, default='BTC-PERP')
@click.option("--price", type=str, default='9500')
@click.option("--qty", type=str, default='0.1')
@click.option("--order-type", type=str, default="limit")
@click.option("--side", type=click.Choice(['buy', 'sell']), default='buy')
@click.option("--time-in-force", type=click.Choice(['GTC', 'IOC', 'IOO']), default="GTC")
@click.option("--resp-inst", type=click.Choice(['ACK', 'ACCEPT', 'DONE']), default="ACCEPT")
@click.option("--time-in-force", type=click.Choice(['GTC', 'IOC', 'IOO']), default="GTC")
@click.option('--verbose/--no-verbose', default=False)
<<<<<<< HEAD
def run(config, symbol, price, qty, order_type, side, resp_inst, time_in_force, verbose):
=======
def run(config, symbol, price, qty, order_type, side, time_in_force, resp_inst, verbose):
>>>>>>> f8ce177db698aaa146577d14377c2b48dadb85cd
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    url = f"{host}/{group}/api/pro/v1/futures/order"

    ts = utc_timestamp()
    order = dict(
        id = uuid32(),
        time = ts,
        symbol = symbol,
        orderPrice = str(price),
        orderQty = str(qty),
        orderType = order_type,
        side = side.lower(),
        timeInForce = time_in_force,
        respInst = resp_inst,
    )

    if verbose:
        print(f"url: {url}")
        print(f"order: {order}")

    headers = make_auth_headers(ts, "order", apikey, secret)
    res = requests.post(url, headers=headers, json=order)

    pprint(parse_response(res))



if __name__ == "__main__":
    run()
