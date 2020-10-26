"""
扩展
"""
from flask_cors import CORS
from flask_redis import FlaskRedis

cors = CORS(supports_credentials=True)
redis_client = FlaskRedis()
