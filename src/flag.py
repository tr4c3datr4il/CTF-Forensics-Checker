from zlib import crc32
from hashlib import md5, sha1

salt = b'hehe'

FLAG = "FLAG{{this_is_an_example_flag{}}}".format(
    crc32(salt)
)