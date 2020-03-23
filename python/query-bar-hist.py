import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *

@click.command()
@click.option("--symbol", type=str, default="BTC-PERP")
@click.option("--interval", type=str, default="1")
@click.option("--frm", type=int)
@click.option("--to", type=int)
@click.option("--n", type=int, default=10)
@click.option("--config", type=str, default="config.json")
@click.option('--verbose/--no-verbose', default=False)
def run(symbol, interval, frm, to, n, config, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
  
    url = f"{host}/api/pro/v1/barhist"
    params = {
        "symbol":   symbol,
        "interval": interval,
        "n":        n,
        "from":     frm,
        "to":       to,
    }

    if verbose:
        print(f"url = {url}")
        print(f"params = {params}")

    res = requests.get(url, params = params)
    pprint(parse_response(res))


if __name__ == "__main__": 
    run()  