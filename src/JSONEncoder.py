from eth_utils.conversions import to_hex
from json import JSONEncoder

class BytesJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return to_hex(o)
        else:
            return super(BytesJSONEncoder, self).default(o)