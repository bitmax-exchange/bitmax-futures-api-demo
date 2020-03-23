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
@click.option("--order-id", type=str, required=True, help="order id (provided by server when placing order) to cancel")
@click.option('--print-only/--no-print-only', default=True, help="if --print-only is enabled (as default), the script will not make the actual API call. It will only print request body.")
def run(config, symbol, order_id, print_only):
    """Send batch orders. 

    You can use this script to cancel multiple orders within the same API call. 

    All order parameters should be a comma separated list. For instance, the API call
    below will try to cancel two orders with id abc123 and xyz789, respectively

      python <script-name> --symbol BTC-PERP,BTC-PERP --order-id abc123,xyz789

    Please note if a parameter has only one value, you can simplify it by writing it only once, 
    thus the script above can also be written as:

      python <script-name> --symbol BTC-PERP --order-id abc123,xyz789

    The default behavior of this script is to only print the request body. To send out the actual 
    request, please add the --no-print-only flag.
    """
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    group = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{group}/api/pro/v1/futures/order/batch"

    ts = utc_timestamp()


    orders = []
    for (sym, orderId) in np.broadcast(*[L(x) for x in [symbol, order_id]]):
        orders.append(dict(
            time = ts,
            symbol = sym,
            orderId = orderId
        ))

    req = dict(orders = orders)

    print(f"request url: {url}")
    print("request body:\n    ")
    pprint(req)

    if print_only: 
        print("\nTo send out this request, please add flag --no-print-only")
    else:
        headers = make_auth_headers(ts, "order/batch", apikey, secret)
        res = requests.delete(url, headers=headers, json=req)

        pprint(parse_response(res))



if __name__ == "__main__":
    run()
