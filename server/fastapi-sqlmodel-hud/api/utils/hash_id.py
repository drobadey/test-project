import hashlib
import re

import unidecode

'''
 See https://github.com/HUD-Data-Lab/Data.Exchange.and.Interoperability/issues/26
 This implimentation works; however, it may not be the correct approach 
 (see comment on issue dated Aug 9, 2024  
'''

DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def encode_base62_num(integer, base=DIGITS):
    if integer == 0:
        return base[0]

    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        # For Python 2 use /= instead of //=:
        # integer /= length
        integer //= length

    return ret

def encodebytes(barray):
    return encode_base62_num(int.from_bytes(barray, "big"))

def hash_str_base62(s):
    sha1 = hashlib.sha1(s.encode()).digest()
    return encodebytes(sha1)

def normalize(s):
    # normalize "José" to "JOSE"
    s = unidecode.unidecode_expect_ascii(s).upper()
    # normalize "JOHNSON-JACKSON" to "JOHNSONJACKSON"
    return re.sub(r'[^.a-zA-Z0-9]', "", s)

def create_hash_id(first_name: str, last_name: str, full_ssnum: str, date_of_birth: str) -> str:
    id_str = f"{normalize(full_ssnum)} {normalize(last_name)} {normalize(first_name[-1:])} {normalize(date_of_birth)}"
    return hash_str_base62(id_str)
