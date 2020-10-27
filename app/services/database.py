from app.extensions import redis_client
from app.config.config import RedisConfig


def get_jsapi_ticket() -> str:
    """
    从 redis 中获取jsapi ticket
    """

    return redis_client.get(RedisConfig.Key.jsapi_ticket)


def get_access_token() -> str:
    """
    从 redis 中获取 access_token
    """

    return redis_client.get(RedisConfig.Key.access_token)


def set_jsapi_ticket(ticket, ex=None):
    """
    将 jsapi ticket 存入 redis 中

    :param ticket: 微信返回的 ticket
    :param ex: 过期时间，微信返回的 expires_in，单位为秒，过期时间减60秒保证及时刷新
    """

    redis_client.set(RedisConfig.Key.jsapi_ticket, ticket, ex=ex - 60 if ex else ex)


def set_access_token(access_token, ex=None):
    """
    将 access_token 存入 redis 中

    :param access_token: 微信返回的 access_token
    :param ex: 过期时间，微信返回的 expires_in，单位为秒，过期时间减60秒保证及时刷新
    """

    redis_client.set(RedisConfig.Key.access_token, access_token, ex=ex - 60 if ex else ex)
