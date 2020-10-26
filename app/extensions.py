"""
扩展
"""
from flask_cors import CORS
from flask_redis import FlaskRedis
from redis import StrictRedis
import typing

cors = CORS(supports_credentials=True)

redis_client: typing.Union[StrictRedis, FlaskRedis] = FlaskRedis()
