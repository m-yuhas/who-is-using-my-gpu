from typing import Dict, List


import argparse
import datetime
import json
import logging
import time


import coloredlogs
import mariadb
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


def log_stats(host, gpu_data, proc_data, timestamp) -> None:
    connection = mariadb.connect(
        host='mysql',
        port=3306,
        user='coordinator',
        password='bar',
        database='gpu_db',
    )
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO gpu_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            timestamp,
            host,
            gpu_data['id'],
            gpu_data['type'],
            gpu_data['fan_speed'],
            gpu_data['temperature'],
            gpu_data['mode'],
            gpu_data['power_used'] / 1e3,
            gpu_data['power_total'] / 1e3,
            gpu_data['memory_used'] / 2 ** 20,
            gpu_data['memory_total'] / 2 ** 20,
            json.dumps([p for p in proc_data if p['gpu'] == gpu_data['id']])
        )
    )
    connection.close() #TODO: try-finally this


def log_errors(host, error_data) -> None:
    connection = mariadb.connect(
        host='mysql',
        port=3306,
        user='coordinator',
        password='bar',
        database='gpu_db',
    )
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO errors VALUES (?, ?, ?)',
        (timestamp, host, json.dumps(error_data))
    )
    connection.close()


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
                LOGGER.debug('Obtained response from host...') 
                LOGGER.debug(response.json())
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for gpu in response.json()['gpus']:
                    log_stats(host, gpu, response.json()['procs'], timestamp)
                if len(response.json()['errors']) > 0:
                    log_errors(host, gpu, timestamp)
            except Exception as err:
                LOGGER.error(f'{type(err).__name__} occurred probing {address}')
                LOGGER.error(f'{err}')
        LOGGER.info('Going to sleep...')
        long_sleep(args.period)

