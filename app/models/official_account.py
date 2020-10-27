"""
公众号
"""
import requests
import random
import string
import time
import hashlib
import base64
import io
import typing
import json

from app.models import CurrentUser
from app.config import WeChatConfig
from app.extends.helper import manage_wechat_error
from app.extends.error import HttpError
from app.services import database


class OfficialAccount(object):
    @property
    def access_token(self):
        """
        access_token是公众号的全局唯一接口调用凭据，公众号调用各接口时都需使用access_token。
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html
        """

        access_token = database.get_access_token()
        if access_token is None:
            return self.refresh_token()
        return access_token

    @property
    def jsapi_ticket(self):
        """
        jsapi_ticket是公众号用于调用微信JS接口的临时票据。
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        """

        ticket = database.get_jsapi_ticket()
        if ticket is None:
            return self.refresh_jsapi_ticket()
        return ticket

    @property
    def user_info(self) -> dict:
        """
        关注公众号的用户的信息，相比于网页授权获取的信息更加详细
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

        data, errcode = self.get_subscribe_user_info()

        if errcode is not None:
            if errcode == 40014:  # access_token无效
                self.refresh_token()
                data, errcode = self.get_subscribe_user_info()

            if errcode == 40003:  # openid不属于该公众号或用户未关注
                raise HttpError(403, '请先关注公众号')

            manage_wechat_error(data, [], '获取公众号用户信息失败')

        return data

    def get_jssdk_config_data(self, url) -> dict:
        """
        获取 jssdk 所需要的配置信息
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        """

        jsapi_ticket = self.jsapi_ticket
        noncestr = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        timestamp = int(time.time())

        signature = hashlib.sha1(
            f'jsapi_ticket={jsapi_ticket}&noncestr={noncestr}&timestamp={timestamp}&url={url}'.encode(
                'utf-8')).hexdigest()

        return {
            'signature': signature,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'appid': WeChatConfig.APP_ID
        }

    def get_subscribe_user_info(self) -> typing.Tuple[dict, str]:
        """
        获取关注公众号的用户的信息
        https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        GET https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        """

        user = CurrentUser()
        resp = requests.get(WeChatConfig.get_subscribe_user_info_url(self.access_token, user.openid))
        data: dict = json.loads(resp.content)

        return data, data.get('errcode')

    def get_jsapi_ticket(self):
        """
        获取 jsapi_ticket
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        GET https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi
        """

        resp = requests.get(WeChatConfig.get_jsapi_ticket(self.access_token))

        return json.loads(resp.content)

    @staticmethod
    def refresh_token():
        """
        刷新公众号 access_token
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html
        GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
        """

        resp = requests.get(WeChatConfig.refresh_access_token_url())
        data: dict = json.loads(resp.content)

        manage_wechat_error(data, [], '刷新 access_token 失败')

        database.set_access_token(data.get('access_token', data.get('expires_in')))

        return data.get('access_token')

    def refresh_jsapi_ticket(self):
        """
        刷新 jsapi_ticket
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        GET https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi
        """

        data: dict = self.get_jsapi_ticket()

        if 'ticket' not in data:
            if data.get('errcode') == 40014:  # access_token无效
                self.refresh_token()
                data, _ = self.get_jsapi_ticket()

            manage_wechat_error(data, [], '获取 jsapi_ticket 失败')

        database.set_jsapi_ticket(data.get('ticket'), data.get('expires_in'))

        return data.get('ticket')

    def get_media(self, media_id):
        """
        下载多媒体文件
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_temporary_materials.html

        :param media_id: 前端传来的媒体文件ID
        """

        resp, content_type = self.get_media_resp(media_id)

        if content_type == 'application/json' or content_type == 'text/plain':  # Content-Type 不是媒体类型，说明请求出错，判断错误码
            data: dict = json.loads(resp.content)
            if data.get('errcode') == 40014:  # access_token过期
                self.refresh_token()
                resp, content_type = self.get_media_resp(media_id)
                if content_type == 'application/json' or content_type == 'text/plain':
                    data: dict = json.loads(resp.content)
            if data.get('errcode') == 40007:  # 不合法的媒体文件id
                raise HttpError(400, 'media_id无效')

            manage_wechat_error(data, [], '下载媒体文件失败')

        encoded_media = base64.b64encode(io.BytesIO(resp.content).read()).decode('ascii')

        return {
            'media_data': encoded_media,
            'content_type': resp.headers.get('Content-Type')
        }

    def get_media_resp(self, media_id) -> typing.Tuple[requests.Response, str]:
        """
        发送下载多媒体文件请求
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_temporary_materials.html
        GET https://api.weixin.qq.com/cgi-bin/media/get?access_token=ACCESS_TOKEN&media_id=MEDIA_ID

        :param media_id: 前端传来的媒体文件ID
        """

        resp = requests.get(WeChatConfig.get_media_url(self.access_token, media_id))

        return resp, resp.headers.get('Content-Type')
