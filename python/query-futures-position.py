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
    grp = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{grp}/api/pro/v1/futures/position"

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "futures/position", apikey, secret)

    if verbose: 
        print(f"url = {url}")

    res = requests.get(url, headers=headers)
    # import ipdb; ipdb.set_trace()
    pprint(parse_response(res))

    if verbose:
        pprint(res.headers)


if __name__ == "__main__":
    run()
