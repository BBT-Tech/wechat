"""
公众号
"""
import requests

from app.models import CurrentUser
from app.config import WeChatConfig
from app.extensions import redis_client
from app.extends.helper import manage_wechat_error
from app.extends.error import HttpError


class OfficialAccount(object):
    def __init__(self):
        pass

    @property
    def access_token(self):
        access_token = redis_client.get('access_token')
        if access_token is None:
            return self.refresh_token()
        return access_token

    @property
    def user_info(self) -> dict:
        """
        关注公众号的用户的信息
        https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        {
            "subscribe": 1,
            "openid": "OPENID",
            "nickname": "NICKNAME",
            "sex": "1",
            "language": "zh_CN",
            "city": "广州",
            "province": "广东",
            "country": "中国",
            "headimgurl":"https://headimg.url",
            "subscribe_time": 1382694957,
            "unionid": "UNIONID"
            "remark": "",
            "groupid": 0,
            "tagid_list":[128,2],
            "subscribe_scene": "ADD_SCENE_QR_CODE",
            "qr_scene": 98765,
            "qr_scene_str": ""
        }
        """

        data: dict = self.get_user_info()
        errcode: int = data.get('errcode')

        if errcode is not None:
            if errcode == 40014:  # access_token无效
                self.refresh_token()
                data: dict = self.get_user_info()
                errcode: int = data.get('errcode')

            if errcode == 40003:
                raise HttpError(403, '请先关注公众号')

            manage_wechat_error(data, [], '获取公众号用户信息失败')

        return data

    def get_user_info(self) -> dict:
        """
        获取关注公众号的用户的信息
        https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        GET https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        """
        user = CurrentUser()
        resp = requests.get(WeChatConfig.get_sub_user_info_url(self.access_token, user.openid))

        return resp.json()

    def refresh_token(self):
        """
        刷新 access_token
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html

        """

        pass
