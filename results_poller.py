"""
function for polling reopt api results url
"""
import requests
import json
import time
from logger import log


def poller(url, poll_interval=2):
    """
    Function for polling the REopt API results URL until status is not "Optimizing..."
    :param url: results url to poll
    :param poll_interval: seconds
    :return: dictionary response (once status is not "Optimizing...")
    """
    key_error_count = 0
    key_error_threshold = 4
    status = "Optimizing..."
    log.info(f"Polling {url} for results with interval of {poll_interval}s...")
    while True:

        resp = requests.get(url=url)
        resp_dict = json.loads(resp.content)

        try:
            status = resp_dict['outputs']['Scenario']['status']
        except KeyError:
            key_error_count += 1
            log.info(f'KeyError count: {key_error_count}')
            if key_error_count > key_error_threshold:
                log.info(
                    f'Breaking polling loop due to KeyError count threshold of {key_error_threshold} exceeded.'
                )
                break

        if status != "Optimizing...":
            break
        else:
            time.sleep(poll_interval)

    return resp_dict
