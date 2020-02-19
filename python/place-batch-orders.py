import os
import click
import requests
from pprint import pprint
import numpy as np

# Local imports 
from util import *


def L(s: str) -> list: 
    return s.split(",")



@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--symbol", type=str, default='BTC-PERP', help="symbol")
@click.option("--price", type=str, default='9500', help="price")
@click.option("--qty", type=str, default='0.1', help="quantity")
@click.option("--order-type", type=click.Choice(['limit', 'market', 'stop_limit', 'stop_market']), default="limit", help="order type, default limit")
@click.option("--side", type=click.Choice(['buy', 'sell']), default='buy')
@click.option("--time-in-force", type=click.Choice(['GTC', 'IOC', 'FOK', 'IOO']), default="GTC", help="GTC - Good till Canceled, IOC - Immediate or Cancel, FOK - Fill or Kill, IOO - Immediate or OTC")
@click.option("--resp-inst", type=click.Choice(['ACK', 'ACCEPT', 'DONE']), default="ACCEPT")
@click.option('--print-only/--no-print-only', default=True, help="if --print-only is enabled (as default), the script will not make the actual API call. It will only print request body.")
def run(config, symbol, price, qty, order_type, side, time_in_force, resp_inst, print_only):
    """Send batch orders. 

    You can use this script to place multiple orders within the same API call. 

    All order parameters should be a comma separated list. For instance, the API call
    below will generte two limit orders: buy 1 BTC-PERP at 9000 and buy 2 BTC-PERP at 9100. 

      python <script-name> --symbol BTC-PERP,BTC-PERP --price 9000,9100 --qty 1,2 --side buy,buy

    Please note if a parameter has only one value, you can simplify it by writing it only once, 
    thus the script above can also be written as:

      python <script-name> --symbol BTC-PERP --price 9000,9100 --qty 1,2 --side buy

    The default behavior of this script is to only print the request body. To send out the actual 
    request, please add the --no-print-only flag.
    """
    if config is None:
        config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
        print(f"Config file is not specified, use {config}")
    btmx_cfg = load_config(config)['bitmax']

    host = btmx_cfg['https']
    group = btmx_cfg['group']
    apikey = btmx_cfg['apikey']
    secret = btmx_cfg['secret']

    url = f"{host}/{group}/api/pro/v1/futures/order/batch"

    ts = utc_timestamp()


    orders = []
    for (sym, px, qty, tp, sd, tif) in np.broadcast(*[L(x) for x in [symbol, price, qty, order_type, side, time_in_force]]):
        orders.append(dict(
            id = uuid32(),
            time = ts,
            symbol = sym,
            orderPrice = px,
            orderQty = qty,
            orderType = tp,
            side = sd.lower(),
            timeInForce = tif,
        ))

    req = dict(orders = orders)

    print(f"request url: {url}")
    print("request body:\n    ")
    pprint(req)
        
    if print_only: 
        print("\nTo send out this request, please add flag --no-print-only")
    else:
        headers = make_auth_headers(ts, "order/batch", apikey, secret)
        res = requests.post(url, headers=headers, json=req)

        pprint(parse_response(res))



if __name__ == "__main__":
    run()
