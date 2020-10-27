"""
自动刷新 access_token 和 jsapi_ticket
"""
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from app import create_app
from app.models import OfficialAccount
from app.extends.error import HttpError

app = create_app()
official_account = OfficialAccount()


def main():
    """
    刷新 jsapi_ticket 和 access_token
    """
    with app.app_context():
        try:
            official_account.refresh_token()
            official_account.refresh_jsapi_ticket()
        except HttpError as e:
            logging.error(str(e.to_dict()))
        except Exception as e:
            logging.error(str(e))


if __name__ == '__main__':
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', seconds=7130)
    scheduler.start()
