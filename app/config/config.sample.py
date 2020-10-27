"""
配置文件
需要修改的数据
AppConfig:
    SECRET_KEY
    REDIS_URL
RedisConfig:
    Key:
        jsapi_ticket
        access_token
WeChatConfig:
    APP_ID
    APP_SECRET
"""
from urllib.parse import quote


class AppConfig:
    SECRET_KEY = '123456'
    REDIS_URL = 'redis://localhost:6379/0'  # redis地址


class RedisConfig:
    # 保存在 redis 中的键名
    class Key:
        jsapi_ticket = 'flask:wechat:jsapi_ticket'
        access_token = 'flask:wechat:access_token'


class WeChatConfig:
    APP_ID = ''  # APPID
    APP_SECRET = ''  # APPSECRET

    API_BASE_URL = "https://api.weixin.qq.com"
    OAUTH_BASE_URL = "https://open.weixin.qq.com/connect"

    @classmethod
    def auth_url(cls, state, redirect_uri, scope='snsapi_userinfo'):
        """
        微信授权链接
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html

        :param state: 授权成功后要返回的前端地址，一般为 encodeURIComponent(window.location.href)
        :param scope: 可选 snsapi_base（获取用户 openid，静默授权）, snsapi_userinfo（获取用户信息，需手动同意）
        :param redirect_uri: 用户同意授权后携带 code 和 state 请求的后端接口
        """

        return f'{cls.OAUTH_BASE_URL}/oauth2/authorize?appid={cls.APP_ID}&redirect_uri={quote(redirect_uri, safe="")}&response_type=code&scope={scope}&state={state}#wechat_redirect'

    @classmethod
    def get_access_token_url(cls, code):
        """
        通过 code 换取网页授权 access_token
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code

        :param code: 用户同意授权后，请求该地址携带的 code
        """

        return f'{cls.API_BASE_URL}/sns/oauth2/access_token?appid={cls.APP_ID}&secret={cls.APP_SECRET}&code={code}&grant_type=authorization_code'

    @classmethod
    def check_access_token_url(cls, access_token, openid):
        """
        判断用户授权的 access_token 有效性
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID

        :param access_token: access_token
        :param openid: 当前用户的 openid
        """

        return f'{cls.API_BASE_URL}/sns/auth?access_token={access_token}&openid={openid}'

    @classmethod
    def refresh_user_access_token_url(cls, refresh_token):
        """
        刷新用户授权的 access_token
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN

        :param refresh_token: 当前用户的 refresh_token
        """

        return f'{cls.API_BASE_URL}/sns/oauth2/refresh_token?appid={cls.APP_ID}&grant_type=refresh_token&refresh_token={refresh_token}'

    @classmethod
    def get_user_info_url(cls, access_token, openid):
        """
        获取用户信息接口
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
        GET https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

        :param access_token: 用户授权获取的 access_token
        :param openid: 当前用户的 openid
        """

        return f'{cls.API_BASE_URL}/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN'

    @classmethod
    def get_sub_user_info_url(cls, access_token, openid):
        """
        获取关注公众号的用户的信息
        https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId
        GET https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

        :param access_token: 微信公众号的 access_token
        :param openid: 当前用户的 openid
        """

        return f'{cls.API_BASE_URL}/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN'

    @classmethod
    def refresh_access_token_url(cls):
        """
        刷新微信公众号的 access_token
        https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html
        GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
        """

        return f'{cls.API_BASE_URL}/cgi-bin/token?grant_type=client_credential&appid={cls.APP_ID}&secret={cls.APP_SECRET}'

    @classmethod
    def get_jsapi_ticket(cls, access_token):
        """
        获取 jsapi_ticket
        https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
        GET https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi

        :param access_token: 微信公众号的 access_token
        """

        return f'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi'

    @classmethod
    def get_media_url(cls, access_token, media_id):
        """
        下载多媒体文件
        https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_temporary_materials.html
        GET https://api.weixin.qq.com/cgi-bin/media/get?access_token=ACCESS_TOKEN&media_id=MEDIA_ID

        :param access_token: 微信公众号的 access_token
        :param media_id: 前端传来的媒体文件ID
        """

        return f'https://api.weixin.qq.com/cgi-bin/media/get?access_token={access_token}&media_id={media_id}'
