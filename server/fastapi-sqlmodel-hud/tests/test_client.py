import unittest

# ModuleNotFoundError: No module named 'api'
# make sure you run from the root directory
from api.utils.hash_id import normalize, create_hash_id, hash_str_base62, encode_base62_num


class TestGenerateId(unittest.TestCase):
    def test_normalize(self):
        result_normalize = normalize(u'José')
        self.assertEqual(result_normalize, 'JOSE', 'normalize() should return JOSE.')

        result_encode_base62_num = encode_base62_num(1)
        self.assertEqual(result_encode_base62_num, '1', 'encode_base62_num(1) failed')

        result_encode_base62_num = encode_base62_num(61)
        self.assertEqual(result_encode_base62_num, 'z', 'encode_base62_num(62) failed')

        result_encode_base62_num = encode_base62_num(62)
        self.assertEqual(result_encode_base62_num, '10', 'encode_base62_num(63) failed')

        # https://github.com/HUD-Data-Lab/Data.Exchange.and.Interoperability/issues/26
        # (see cyberchef reference)
        result_sha1_b62 = hash_str_base62(u'123006789 MCCOYRENE R 07041999')
        self.assertEqual(result_sha1_b62, 'ZLKRmaqw2sASJgXOvJFn0yeOnBi', 'create_id() did no work..')

if __name__ == '__main__':
    unittest.main()
