
import configparser
import logging as log
from tracker import Tracker


CONFIG_NAME = 'cfg.ini'

CFG = configparser.ConfigParser()
CFG.read(CONFIG_NAME)


def extract_telegram_cfg(cfg):
    try:
        api_id = cfg['telegram']['api_id']
        api_hash = cfg['telegram']['api_hash']
        phone = cfg['telegram']['phone']
        return api_id, api_hash, phone
    except KeyError:
        log.error(f'Could not parse telegram section in {CONFIG_NAME}')
        quit(1)


def main():

    api_id, api_hash, phone = extract_telegram_cfg(CFG)

    tr = Tracker(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone
    )

    tr.start()


if __name__ == '__main__':
    main()
