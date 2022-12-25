from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class OrderType(BaseEnum):
    Market = 'MARKET'
    Limit = 'LIMIT'
    Stop = 'STOP'


class OrderSide(BaseEnum):
    Long = 'BUY'
    Short = 'SELL'
