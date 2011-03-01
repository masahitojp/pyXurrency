import urllib2
import json
import datetime
import xurrency.cache

'''
link      http://xurrency.com
'''


class Xurrency(object):
    CURRENCIES_INVALID = 2
    LIMIT_REACHED = 3
    API_KEY_INVALID = 4
    API_KEY_EXPIRED = 5

    CURRENCIES = \
        ["eur", "usd", "gbp", "aud", "brl", "cad", "chf", "cny",
         "dkk", "hkd", "inr", "jpy", "krw", "lkr", "myr", "nzd",
         "sgd", "uwd", "zar", "thb", "sek", "nok", "mxn", "bgn",
         "czk", "uek", "huf", "ltl", "lvl", "pln", "ron", "skk",
         "isk", "hrk", "rub", "try", "php", "cop", "ars", "clp",
         "svc", "tnd", "pyg", "mad", "jmd", "sar", "qar", "hnl",
         "syp", "kwd", "bhd", "egp", "omr", "ngn", "pab", "pen",
         "ils", "uyu", "aed"]

    def __init__(self, key=None, cache_seconds=86400):
        self._key = key
        self._cache = xurrency.cache.CacheWithTimeLimit(cache_seconds)
        self._base_url = 'http://xurrency.com/api/%s/%s/1'

    def get_rate(self, base, target, amount=1):
        rate = self._make_request(base, target)
        return (amount * rate['value'])

    def _make_request(self, base, target):
        if (base not in self.CURRENCIES) or (target not in self.CURRENCIES):
            raise XurrencyError("Invalid currency codes.")

        if self._is_cached(self._create_key(base, target)):
            result = self._get_cache(self._create_key(base, target))
        else:
            api_url = self._base_url % (base, target)
            if self._key:
                api_url += '?key=%s' % (self._key)
            try:
                resp = urllib2.urlopen(api_url)
                data = resp.read()
            except urllib2.HTTPError, error:
                raise XurrencyHTTPError(error)
            except urllib2.URLError as e:
                raise XurrencyURLError(e)

            jsondata = json.loads(data)

            if jsondata['status'] == 'fail':
                response_code = jsondata['code']
                message = jsondata['message']
                if response_code == self.LIMIT_REACHED:
                    if (self._create_key(base, target) \
                            not in self._cache._cache):
                        raise XurrencyAPILimitReachedError(message)
                elif response_code == self.CURRENCIES_INVALID:
                    raise XurrencyAPIInvalidCurrenciesError(message)
                elif response_code == self.API_KEY_INVALID or \
                         response_code == self.API_KEY_EXPIRED:
                    raise XurrencyAPIInvalidKeyError(message)
                else:
                    raise XurrencyError(message)
            else:
                result = jsondata['result']
                self._set_cache(self._create_key(base, target), result,\
                        datetime.datetime.strptime(result['updated_at'],\
                            '%Y-%m-%dT%H:%M:%SZ'))
        return result

    def _create_key(self, base, target):
        return "%s:%s" % (base, target)

    def _set_cache(self, key, value, dt):
        self._cache.set(key, value, dt)

    def _get_cache(self, key):
        return self._cache.get(key)

    def _is_cached(self, key):
        return self._cache.is_cache(key)

    def _flush_cache(self):
        self._cache.flush()


class XurrencyError(Exception):
    """Base class for exceptions in this module."""
    pass


class XurrencyAPILimitReachedError(XurrencyError):
    pass


class XurrencyAPIInvalidCurrenciesError(XurrencyError):
    pass


class XurrencyAPIInvalidKeyError(XurrencyError):
    pass


class XurrencyHTTPError(XurrencyError):
    pass


class XurrencyURLError(XurrencyError):
    pass
