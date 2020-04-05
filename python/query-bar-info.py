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
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']

    url = f"{host}/api/pro/v1/barhist/info"

    if verbose: 
        print(f"url = {url}")

    res = requests.get(url)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()