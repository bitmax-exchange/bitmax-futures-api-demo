import os
import click
import requests
from pprint import pprint

# Local imports 
from util import *


@click.command()
@click.option("--config", type=str, default=None, help="path to the config file")
@click.option("--exec-id", type=int, required=False)
@click.option("--request-id", type=str, required=False)
@click.option('--verbose/--no-verbose', default=False)
def run(config, exec_id, request_id, verbose):
    
    cfg = load_config(get_config_or_default(config))['bitmax']

    host = cfg['https']
    grp = cfg['group']
    apikey = cfg['apikey']
    secret = cfg['secret']

    url = f"{host}/{grp}/api/pro/v1/futures/balance-update"

    ts = utc_timestamp()
    headers = make_auth_headers(ts, "futures/balance-update", apikey, secret)
    params = dict(execId = exec_id, requestId = request_id)

    if verbose: 
        print(f"url = {url}")
        print(f"params = {params}")

    res = requests.get(url, headers=headers, params=params)
    pprint(parse_response(res))


if __name__ == "__main__":
    run()
