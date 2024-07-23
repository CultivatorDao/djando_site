import base64 as b64
import json


class Base64Converter:
    __encoding = "ascii"

    def to_encoding(self, message):
        return message.encode(self.__encoding)

    def encode(self, message):
        return b64.b64encode(self.to_encoding(message)).decode(self.__encoding)

    def decode(self, message):
        return b64.b64decode(self.to_encoding(message)).decode(self.__encoding)

    def dict_to_base64(self, dictionary):
        return self.encode(json.dumps(dictionary))

    def dict_from_base64(self, base64_str):
        return json.loads(self.decode(base64_str))

