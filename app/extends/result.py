import typing


class Result:
    status = 200
    _msg = 'OK'
    _data = None

    @classmethod
    def data(cls, _data: typing.Union[dict, str]):
        cls._data = _data
        return cls

    @classmethod
    def msg(cls, _msg: typing.Union[dict, str]):
        cls._msg = _msg
        return cls

    @classmethod
    def build(cls):
        return {
            'status': cls.status,
            'msg': cls._msg,
            'data': cls._data
        }
