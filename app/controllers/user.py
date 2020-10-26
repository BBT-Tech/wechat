from flask import Blueprint

from app.models import CurrentUser
from app.extends.result import Result

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('')
def get_user_info():
    """
    获取用户信息
    https://developers.weixin.qq.com/doc/offiaccount/User_Management/Get_users_basic_information_UnionID.html#UinonId

    :return: {
        "status": 200,
        "msg": "OK",
        "data": userinfo
    }
    """

    user = CurrentUser()
    return Result.data(user.info).build()
