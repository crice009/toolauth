from random import getrandbits
from base64 import urlsafe_b64encode


def ecrypt_pass():
    # 32 random bytes --> 8x the number of bits
    # https://esphome.io/components/api.html#configuration-variables
    data = str(getrandbits(32 * 8))

    # URL and Filename Safe Base64 Encoding
    urlSafeEncodedBytes = urlsafe_b64encode(data.encode("utf-8"))
    urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")

    return urlSafeEncodedStr


def ota_pass():
    # 32 random bites --> anything that will work as a password
    data = str(getrandbits(32))

    # URL and Filename Safe Base64 Encoding
    urlSafeEncodedBytes = urlsafe_b64encode(data.encode("utf-8"))
    urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")

    return urlSafeEncodedStr
