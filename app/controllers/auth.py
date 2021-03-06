from flask import Blueprint, request, redirect, session
import requests

from app.config.config import WeChatConfig
from app.extends.helper import manage_wechat_error
from app.models import CurrentUser

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('')
def login():
    """
    微信授权
    前端使用 window.location.href 访问此接口

    :param: state: 授权成功后要返回的前端地址，一般为encodeURIComponent(window.location.href)
    :return: 微信授权链接, 302
    """

    state = request.args.get('state')

    return redirect(WeChatConfig.auth_url(state))


@auth_bp.route('/code')
def get_access_token():
    """
    用户授权后访问此接口(redirect_uri)，使用 code 获取 access_token

    :param: code: code作为换取access_token的票据，每次用户授权带上的code将不一样，code只能使用一次，5分钟未被使用自动过期。
    :param: state: 授权成功后要跳转到的地址，即encodeURIComponent(window.location.href)

    :return: 前端传来的state, 302
    """

    code = request.args.get('code')
    state = request.args.get('state')

    resp = requests.get(WeChatConfig.get_access_token_url(code))
    data = resp.json()

    manage_wechat_error(data, [40029], '获取 access_token 失败')  # code无效

    session['openid'] = data.get('openid')
    session['access_token'] = data.get('access_token')
    session['refresh_token'] = data.get('refresh_token')

    return redirect(state)


@auth_bp.route('/user')
def get_user_info():
    """
    获取用户信息
    https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
    GET https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

    :return: {
        "city": "广州",
        "country": "中国",
        "headimgurl": "https://thirdwx.qlogo.cn/mmopen/vi_32/sGgFEwic8uUbjEDMexnwOvVyia1UU23ITZJjjUbZSd7PwKciammPwOUIRibk07u4vsx9Y52kYRA47edjCia4NVHIYFg/132",
        "language": "zh_CN",
        "nickname": "lzk",
        "openid": "OPENID",
        "privilege": [],
        "province": "广东",
        "sex": 1
    }
    """

    user = CurrentUser()

    return user.info


@auth_bp.route('/user/openid')
def get_user_openid():
    """
    获取用户的openid

    :return: {
        "openid": "OPENID"
    }
    """

    user = CurrentUser()

    return {'openid': user.openid}
