"""
自动刷新 access_token 和 jsapi_ticket
"""
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import datetime

from app import create_app
from app.models import OfficialAccount
from app.extends.error import HttpError

app = create_app()
official_account = OfficialAccount()


def logger(msg: str):
    with open('./logs/refresh_error.log', 'a', encoding='utf-8') as f:
        f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {msg} \n')


def main():
    """
    刷新 jsapi_ticket 和 access_token
    """
    with app.app_context():
        try:
            official_account.refresh_jsapi_ticket()
            official_account.refresh_token()
        except HttpError as e:
            logger(str(e.to_dict()))
        except Exception as e:
            logger(str(e))


if __name__ == '__main__':
    if not os.path.exists('./logs/'):
        os.makedirs('logs')
    main()
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=2)
    scheduler.start()
