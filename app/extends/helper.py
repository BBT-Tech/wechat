from flask import current_app

from app.extends.error import HttpError


def logger(message: str, data=None):
    """
    记录错误信息

    :param message: 错误信息
    :param data: 返回值
    """

    current_app.logger.error(f'{message} {data if data else ""}')


def manage_wechat_error(data: dict, login_codes: list, msg: str):
    """
    处理微信返回的错误
    全局错误码：https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Global_Return_Code.html

    :param data: 微信返回的数据，包含errcode和errmsg
    :param login_codes: errcode在这之中时返回401，否则返回500
    :param msg: 执行失败的错误信息，返回给前端、记录在log中
    """

    errcode = data.get('errcode')

    if errcode is None or errcode == 0:
        return
    if errcode == -1:
        raise HttpError(504, '微信服务器超时')
    if errcode in login_codes:
        raise HttpError(401, '请先登录微信')

    logger(msg, data)
    raise HttpError(400, f'{msg}, {data.get("errcode")}')
    # raise HttpError(400, f'{msg} {data}') # 将data返回前端，仅供测试
