from typing import Dict, List


import argparse
import datetime
import json
import logging
import time


import coloredlogs
import pymongo
import requests
import yaml


LOGGER = logging.getLogger(__name__)


def long_sleep(t: int) -> None:
    """Accurately sleep for a long time.

    Args:
        t (int): time to sleep in minutes.
    """
    end = time.time() + t * 60
    rest = t * 60 // 2
    while time.time() < end and rest > 0:
        LOGGER.debug(f'Sleeping for {rest} seconds...')
        time.sleep(rest)
        rest = (end - time.time()) // 2


def send_to_database(data: List[Dict]) -> None:
    CONNECTION_STRING = 'mongodb+srv://user:pass@ipaddr/gpuUtilization'
    client = pymongo.MongoClient(CONNECTION_STRING)
    dbname = client['gpuUtilization']
    collection_name = dbname['utilization']
    collection_name.insert_many(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'Periodically fetch usage data from a fleet of GPUs'
    )
    parser.add_argument(
        '--period',
        type=int,
        default=60,
        help='Period to probe fleet members in minutes.'
    )
    parser.add_argument(
        '--hosts',
        default='hosts.toml',
        help='Path to TOML file containing the hostnames and IP addresses of '
             'all GPUs to probe. This always read before a probe begins, '
             'allowing new GPUs to join the fleet without needing to restart '
             'the service.'
    )
    parser.add_argument(
        '--verbosity',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help='Logging level.'
    )
    args = parser.parse_args()
    coloredlogs.install(level=args.verbosity.upper())
    while True:
        LOGGER.info('Reading host list...')
        hosts = {}
        try:
            with open(args.hosts, 'r') as host_f:
                hosts = yaml.safe_load(host_f.read())
        except Exception as err:
            LOGGER.error(f'{type(err).__name__} occurred loading host list!')
            LOGGER.error(f'{err}')

        for host, address in hosts.items():
            LOGGER.info(f'Probing {host}@{address}...')
            try:
                response = requests.get(f'http://{address}')
                LOGGER.debug('Obtained response from host:') 
                LOGGER.debug(response.json())
            except Exception as err:
                LOGGER.error(f'{type(err).__name__} occurred probing {address}')
                LOGGER.error(f'{err}')


            # Add results to mongo

        LOGGER.info('Going to sleep...')
        long_sleep(args.period)

