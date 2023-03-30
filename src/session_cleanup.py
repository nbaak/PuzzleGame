#!/usr/bin/env python3

import settings
import requests
import logging


def send_to_service():
    r = requests.get(f'http://{settings.ip}:{settings.port}/cleanup/{settings.secret}')
    if r.status_code == 200:
        logging.info("successful send request")
        return True
    
    logging.info("failed to send request")
    return False


if __name__ == '__main__':
    send_to_service()
