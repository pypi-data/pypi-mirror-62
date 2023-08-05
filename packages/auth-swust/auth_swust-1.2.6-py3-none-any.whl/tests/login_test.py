import unittest

from auth_swust import Login
from auth_swust.log import AuthLogger, DEBUG

AuthLogger.setLevel(DEBUG)


class LoginTestEvent(unittest.TestCase):
    def test_auth_fail(self):
        login = Login("5120170000", "000000")
        res, info = login.try_login()
        print(res)
        assert res is False
        print(info)
        assert info == "AuthFail"
