from flask import Blueprint

offiaccount_bp = Blueprint('official_account', __name__, url_prefix='/offiaccount')

@offiaccount_bp.route('/jssdk')
def get_js_sdk_data():
    pass