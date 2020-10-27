from flask import Blueprint, request

from app.extends.result import Result
from app.models import OfficialAccount
from app.extends.error import HttpError

offiaccount_bp = Blueprint('official_account', __name__, url_prefix='/offiaccount')


@offiaccount_bp.route('/jssdk', methods=['post'])
def get_jssdk_config_data():
    """
    获取 JSSDK 中需要的配置信息

    :param: url: 当前页面的地址，不包含#及其后面部分，即 window.location.href.split("#")[0]
    :return: {
        "status": 200,
        "msg": "OK",
        "data": {
            "signature": "63d8242da8214b3028624397be3ee20f3f8e3372",
            "noncestr": "0XMzTvB9GxR6aqJ"
            "timestamp": 1603729399,
            "appid": "123456"
        }
    }
    """

    url = request.get_json(force=True).get('url')

    if url is None:
        raise HttpError(400, '请传入当前页面地址')

    official_account = OfficialAccount()
    jssdk_config_data = official_account.get_jssdk_config_data(url)

    return Result.data(jssdk_config_data).build()


@offiaccount_bp.route('/media')
def get_media():
    """
    下载多媒体文件
    https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Get_temporary_materials.html
    GET https://api.weixin.qq.com/cgi-bin/media/get?access_token=ACCESS_TOKEN&media_id=MEDIA_ID

    :param: media_id: 前端调用微信上传图片或音频接口获取到的localId
    :return: {
        "status": 200,
        "msg": "OK",
        "data": {
            "data": "base64编码的图片或音频"
            "content_type": "微信返回的response中的Content-Type，可由此判断保存文件的后缀名，一般为image/jpeg（图片）或audio/amr（音频）"
        }
    }
    """

    media_id = request.args.get('media_id')

    official_account = OfficialAccount()
    media_data = official_account.get_media(media_id)

    return Result.data(media_data).build()
