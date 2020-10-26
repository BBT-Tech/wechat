"""
扩展
"""
from flask_cors import CORS
from flask_redis import FlaskRedis
from redis import StrictRedis

cors = CORS(supports_credentials=True)
redis_client: StrictRedis = FlaskRedis()
