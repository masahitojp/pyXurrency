from minimock import Mock, restore
import xurrency
import urllib2
from nose.tools import assert_equals, raises, with_setup


class TestXurrency(object):
    def setUp(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"result":{"updated_at":"2010-10-02T02:06:00Z", "value":81,"target":"jpy",
"base":"eur"}, "code":0, "status":"ok"}
'''
            )
        xurrency.urllib2.urlopen = Mock(
            'urlopen', returns=urlopen_result)

    def tearDown(self):
        restore()

    @with_setup(setUp, tearDown)
    def test_get_rate_one(self):
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy'),
            81
            )

    @with_setup(setUp, tearDown)
    def test_get_rate_decimal(self):
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPIInvalidCurrenciesError)
    def test_get_rate_InvalidCurrenciesError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"code": 2, "message": "Currencies are not valid", "status": "fail"}
'''
            )
        xurrency.urllib2.urlopen = Mock(
            'urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPILimitReachedError)
    def test_get_rate_APILimitReachedError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"code": 3,   "status": "fail",
  "message":
  "Limit Reached (10 requests per day). Please adquire a license key"}
'''
            )
        xurrency.urllib2.urlopen = Mock(
            'urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyAPIInvalidKeyError)
    def test_get_rate_APIInvalidKeyError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"code": 4, "status": "fail",
  "message": "The api key is not valid"}
'''
            )
        xurrency.urllib2.urlopen = Mock(
            'urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyError)
    def test_get_rate_XurrencyError(self):
        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"code": 1, "status": "fail",
  "message": "Amount should be between 0 and 999999999"}
'''
            )
        xurrency.urllib2.urlopen = Mock(
            'urlopen', returns=urlopen_result)
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(setUp, tearDown)
    @raises(xurrency.XurrencyError)
    def test_get_rate_XurrencyError_InvalidCurrency(self):
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('invalid', 'jpy', 37.2),
            81 * 37.2
            )

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyURLError)
    def test_get_rate_URLError(self):
        xurrency.urllib2.urlopen = \
                Mock('urlopen', raises=urllib2.URLError(''))
        pyx = xurrency.Xurrency()
        pyx.get_rate('eur', 'jpy')

    @with_setup(teardown=tearDown)
    @raises(xurrency.XurrencyHTTPError)
    def test_get_rate_HTTPError(self):
        xurrency.urllib2.urlopen = \
                Mock('urlopen', \
                raises=urllib2.HTTPError('url', 401, '', {}, None))
        pyx = xurrency.Xurrency()
        pyx.get_rate('eur', 'jpy')

    @with_setup(setUp, tearDown)
    def test_get_rate_WithValue_InvalidCurrenciesError(self):
        """
        Even if XurrencyAPIInvalidCurrenciesError is returned after execute,
        the value has already been used if it has cached it.
        """
        pyx = xurrency.Xurrency()
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )

        urlopen_result = Mock('urlobject')
        urlopen_result.read = Mock(
            'urlobj.read', returns='''
{"code": 4, "status": "fail",
  "message": "The api key is not valid"}
''')
        assert_equals(
            pyx.get_rate('eur', 'jpy', 37.2),
            81 * 37.2
            )
