from time import sleep
from datetime import datetime
import shutil

from pyrogram import (
    Client, UserStatus, UserStatusHandler, DeletedMessagesHandler, Messages, Message,
    Dialog
)
import schedule as sch
import logging as log

from db import (
    tracker_session, UserInfo, UserInfoHistory, LastOnline, OnlineHistory
)

from utils import (
    get_user_bio, rows_equal, timer, get_rows_difference, parse_user_status,
    parse_message
)


class Tracker:
    def __init__(self, api_id, api_hash, phone):
        self.client = Client(
            session_name='session',
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone
        )

        self.bulk = []

    @timer
    def update_user_info(self):
        all_users = self.client.get_contacts()

        user_info_changed_count = 0

        for user in all_users:
            user_row_dict = {
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_name': user.username,
                'bio': get_user_bio(user.username),
                'trackable_online': any([user.status.online, user.status.date]),
                'last_modified': datetime.now()
            }

            db_user: UserInfo = tracker_session.query(UserInfo).filter(
                UserInfo.user_id == user.id
            ).scalar()

            if db_user is None:  # if there are no such user in db
                tracker_session.add(
                    UserInfo(**user_row_dict)
                )
            elif not rows_equal(  # if there are such user in db
                    db_user,      # but the info has changed
                    UserInfo(**user_row_dict),
                    skip_fields=('last_modified',)
            ):
                user_info_changed_count += 1
                diffs = get_rows_difference(
                    db_user,
                    UserInfo(**user_row_dict),
                    skip_fields=('last_modified',)
                )
                for diff in diffs:  # find what changed and write difference
                    tracker_session.add(
                        UserInfoHistory(
                            user_id=user.id,
                            time=datetime.now(),
                            changed_field=diff[0],
                            old_value=diff[1],
                            new_value=user_row_dict[diff[0]]
                        )
                    )
                for k, v in user_row_dict.items():
                    setattr(db_user, k, v)

        tracker_session.flush()

        if user_info_changed_count:
            log.warn(f'While updating user info {user_info_changed_count} users'
                     f' changed info')

    def on_changed_status(self, _: Client, user_status: UserStatus):
        user = tracker_session.query(LastOnline).filter(
            LastOnline.user_id == user_status.user_id
        ).scalar()

        new_status = parse_user_status(user_status)

        if user is None:
            tracker_session.add(
                LastOnline(
                    user_id=user_status.user_id,
                    time=datetime.now(),
                    last_status=new_status
                )
            )
            tracker_session.flush()
        elif user.last_status == new_status:
            log.warn('User online status was doubled, skipping'
                     f' uid: {user_status.user_id}')
            # TODO: sometimes we dont get a message about someone going offline
            # TODO: make sure we dont leave someone hanging online for 100 hours
            # TODO: because of unclosed online status
            # Hint: if we get doubled message just save that online sess as
            # 300 secs sess
        else:
            log.warn(f'User {user_status.user_id} is now {new_status}')
            user.last_status = new_status
            self.bulk.append(
                OnlineHistory(
                    user_id=user_status.user_id,
                    time=datetime.now(),
                    new_status=new_status
                )
            )
            tracker_session.flush()

    @timer
    def flush_bulk(self):
        tracker_session.bulk_save_objects(self.bulk)
        self.bulk.clear()

    @timer
    def update_user_photos(self):
        shutil.rmtree('pics/')
        for contact in self.client.get_contacts():
            photos = self.client.get_user_profile_photos(contact.id).photos
            if not len(photos):
                continue
            st = photos[0]
            self.client.download_media(
                message=st,
                file_name=f'pics/{contact.id}.jpg'
            )

    def start(self):
        self.client.add_handler(UserStatusHandler(self.on_changed_status))

        sch.every(1).minute.do(self.update_user_info)
        sch.every(1).minute.do(self.flush_bulk)
        sch.every(6).hours.do(self.update_user_photos)

        self.client.start()

        while True:
            sch.run_pending()
            sleep(0.5)
