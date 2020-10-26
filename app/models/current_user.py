"""
当前登录用户
"""

from flask import session
import requests

from app.config import WeChatConfig
from app.extends.error import HttpError
from app.extends.helper import manage_wechat_error


class CurrentUser(object):
    def __init__(self):
        self.check_login()

    @staticmethod
    def check_login():
        """
        判断用户是否登录，需要的信息是否在 session 中
        """
        if not {'openid', 'access_token', 'refresh_token'} <= set(session):
            raise HttpError(401, '请先登录')

    @property
    def access_token(self):
        return session.get('access_token') if self.check_access_token() else self.refresh_access_token()

    @property
    def openid(self):
        return session.get('openid')

    @property
    def refresh_token(self):
        return session.get('refresh_token')

    @property
    def info(self) -> dict:
        """
        获取用户信息
        https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        GET https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

        :return 用户信息
        {
            "openid": "OPENID",
            "nickname": "NICKNAME",
            "sex": "1",
            "province": "PROVINCE",
            "city": "CITY",
            "country": "COUNTRY",
            "headimgurl": "https://headimg.url",
            "privilege": ["PRIVILEGE1", "PRIVILEGE2"],
            "unionid": "UNIONID"
        }
        """

        resp = requests.get(WeChatConfig.get_user_info_url(self.access_token, self.openid))
        data: dict = resp.json()

        manage_wechat_error(data, [40003, 40014], '获取用户信息失败')  # 不合法的 openid 或 access_token

        return data

    def check_access_token(self) -> bool:
        """
        判断 access_token 有效性
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID

        :return 有效则返回 True，否则返回 False
        """

        resp = requests.get(WeChatConfig.check_access_token_url(self.access_token, self.openid))
        data: dict = resp.json()

        return data.get('errcode') == 0

    def refresh_access_token(self) -> str:
        """
        刷新 access_token
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN

        :return 新的 access_token
        """

        resp = requests.get(WeChatConfig.refresh_access_token_url(self.refresh_token))
        data: dict = resp.json()

        manage_wechat_error(data, [40030], '刷新 access_token 失败')  # refresh_token过期

        session['access_token'] = data.get('access_token')
        session['refresh_token'] = data.get('refresh_token')

        return session.get('access_token')
