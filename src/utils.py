from bs4 import BeautifulSoup
import requests
import logging as log
from time import time

from pyrogram import UserStatus, Message


def get_user_bio(username):
    if not username:
        return None
    resp = requests.get(
        f'https://t.me/{username}'
    )
    if resp.status_code != 200:
        return None

    soup = BeautifulSoup(resp.content, 'html.parser')
    div = soup.find('div', {'class': 'tgme_page_description'})
    return ''.join(div.contents) if div else None


def _parse_row(row, skip_fields):
    return {
        k: v
        for k, v in row.__dict__.items()
        if not k.startswith('_') and k not in skip_fields
    }


def rows_equal(row1, row2, skip_fields=()):
    return _parse_row(row1, skip_fields) == _parse_row(row2, skip_fields)


def get_rows_difference(row1, row2, skip_fields=()):
    row1_parsed = _parse_row(row1, skip_fields)
    row2_parsed = _parse_row(row2, skip_fields)
    if row1_parsed.keys() != row2_parsed.keys():
        raise Exception('Compared dict keys are not the same')

    diff = set(row1_parsed.items()) - set(row2_parsed.items())
    return list(diff)


def timer(function):
    def deco(*args, **kwargs):
        log.warn(f'Started {function.__code__.co_name}')
        t = time()
        function(*args, **kwargs)
        passed = time() - t
        log.warn(f'Finished {function.__code__.co_name} in {round(passed, 2)} seconds')
    return deco


def parse_user_status(status: UserStatus):
    if status.online:
        return 'online'
    if status.date:
        return 'offline'
    if status.recently:
        return 'recently'

