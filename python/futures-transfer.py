import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--asset", type=str, default=None, help="asset code, must be futures collateral asset")
@click.option("--amount", type=str, default=None, help="amount to transfer")
@click.option("--tx-type", type=click.Choice(["withdraw", "deposit"]), required=True, 
    help="Use deposit to transfer asset from cash account into futures account; use withdraw to transfer token from futures account into cash account")
@click.option('--verbose/--no-verbose', default=False)
def run(config, asset, amount, tx_type, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    grp = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{grp}/api/pro/v1/futures/transfer/{tx_type}"

    ts = utc_timestamp()
    headers = make_auth_headers(ts, f"futures/transfer/{tx_type}", apikey, secret)
    json = dict(asset = asset, amount = amount)

    if verbose: 
        print(f"url: {url}")
        print(f"body: {json}")

    res = requests.post(url, headers=headers, json=json)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
