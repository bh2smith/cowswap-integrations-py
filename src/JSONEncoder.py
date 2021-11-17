from eth_utils.conversions import to_hex
from json import JSONEncoder

#class to encode hexbytes into string. For example: appData cant be encoded into JSON
#because its hexbytes, this class encodes it into hex (normal string)
class BytesJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return to_hex(o)
        else:
            return super(BytesJSONEncoder, self).default(o)