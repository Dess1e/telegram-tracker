import logging as log
from tracker import Tracker
from cfg import get_cfg, extract_telegram_cfg


log.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=log.WARN
)


def main():
    api_id, api_hash, phone = extract_telegram_cfg(get_cfg())

    tr = Tracker(
        api_id=api_id,
        api_hash=api_hash,
        phone=phone
    )

    tr.start()


if __name__ == '__main__':
    main()
