from enum import Enum

class Method(Enum):
    DIRECT = 'direct'
    OPENAI = 'openai'

DEFAULT_METHOD = Method.DIRECT
ALLOWED_METHODS = {m.value for m in Method}