from time import sleep
from pyrogram import Client, UserStatus, UserStatusHandler
import schedule as sch

from db import engine


def parse_online_status(client: Client, user_status: UserStatus):
    [usr] = client.get_users([user_status.user_id])
    if user_status.online:
        print(usr.first_name, usr.last_name, 'is now online')
    else:
        print(usr.first_name, usr.last_name, 'has gone offline')


class Tracker:
    def __init__(self, api_id, api_hash, phone):
        self.client = Client(
            session_name='session',
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone
        )
        self.users = None

    def init(self):
        self.users = {
            u.id: u for u in self.client.get_contacts() if not u.status.recently
        }

    def update_user_info(self):
        all_users = self.client.get_contacts()
        for user in all_users:
            engine.query()

    def start(self):
        self.client.add_handler(UserStatusHandler(parse_online_status))
        self.client.start()

        sch.every(2).seconds.do()

        while True:
            sch.run_pending()
            sleep(0.5)

