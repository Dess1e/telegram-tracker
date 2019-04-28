import configparser
import logging as log


CONFIG_NAME = 'cfg.ini'


def get_cfg():
    cfg = configparser.ConfigParser()
    cfg.read(CONFIG_NAME)
    return cfg


def extract_telegram_cfg(cfg):
    try:
        api_id = cfg['telegram']['api_id']
        api_hash = cfg['telegram']['api_hash']
        phone = cfg['telegram']['phone']
        return api_id, api_hash, phone
    except KeyError:
        log.error(f'Could not parse telegram section in {CONFIG_NAME}')
        quit(1)


def extract_db_cfg(cfg):
    try:
        db = cfg['postgres']['db_name']
        user = cfg['postgres']['db_user']
        passwd = cfg['postgres']['db_pass']
        return db, user, passwd
    except KeyError:
        log.error(f'Could not parse postgres section in {CONFIG_NAME}')
        quit(1)

