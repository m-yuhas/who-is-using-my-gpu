import argparse
import datetime
import json
import logging
import time


import coloredlogs
import pymongo
import requests
import yaml


def long_sleep(t: int) -> None:
    """Accurately sleep for a long time.

    Args:
        t (int): time to sleep in minutes.
    """
    end = time.time() + t * 60
    rest = t * 60 // 2
    while time.time() < end and rest > 0:
        logger.debug(f'Sleeping for {rest} seconds...')
        time.sleep(rest)
        rest = (end - time.time()) // 2
        

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
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG')

    while True:
        logger.info('Reading host list...')
        hosts = {}
        try:
            with open(args.hosts, 'r') as host_f:
                hosts = yaml.safe_load(host_f.read())
        except Exception as err:
            logger.error(f'{type(err).__name__} occurred!')
            logger.error(f'{err}')

        for host, address in hosts.items():
            logger.info(f'Probing {host}@{address}...')
            response = requests.get(f'http://{address}')
            logger.debug(response.json())


            # Add results to mongo

        logger.info('Going to sleep...')
        long_sleep(args.period)

