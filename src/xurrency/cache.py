import datetime


class TimeValue(object):
    def __init__(self, value, dt):
        self.value = value
        self.datetime = dt


class CacheWithTimeLimitError(Exception):
    pass


class CacheWithTimeLimit(object):
    def __init__(self, seconds=0):
        """
        >>> c = CacheWithTimeLimit(-1)
        Traceback (most recent call last):
        ...
        CacheWithTimeLimitError: Please specify the value of 0 or more.

        """
        if seconds < 0:
            raise CacheWithTimeLimitError(\
                    "Please specify the value of 0 or more.")
        self._cache = {}
        self._seconds = seconds

    def __iter__(self):
        return self

    def is_cache(self, key, dt=datetime.datetime.utcnow()):
        """
        >>> c = CacheWithTimeLimit(100)
        >>> c.is_cache("key")
        False
        >>> c.set("key", "value")
        >>> c.is_cache("key")
        True
        """
        if key in self._cache:
            add_data_time = dt - self._cache[key].datetime
            cache_seconds = datetime.timedelta(seconds=self._seconds)
            if add_data_time >= cache_seconds:
                return False
            else:
                return True
        else:
            return False

    def get(self, key):
        """
        >>> c = CacheWithTimeLimit()
        >>> c.set("key", "value")
        >>> c.get("key")
        'value'
        """
        return self._cache[key].value

    def set(self, key, value, dt=datetime.datetime.utcnow()):
        """
        Add Data.

        The cash time is assumed to be 100 seconds.
        >>> c = CacheWithTimeLimit(100)
        >>> nt = datetime.datetime.utcnow()
        >>> c.set("key", "value", nt)
        >>> c._cache["key"].value
        'value'
        >>> c._cache["key"].datetime == nt
        True

        The value is not updated until the cash time passes.
        >>> c.set("key", "new_value",nt)
        >>> c.get("key")
        'value'

        When the cash time passes, the value is updated.
        >>> c.set("key", "new_value2", nt+datetime.timedelta(seconds=101))
        >>> c.get("key")
        'new_value2'
        """
        if not self.is_cache(key, dt):
            dv = TimeValue(value, dt)
            self._cache[key] = dv

    def delete(self, key):
        """
        Delete cache data.

        >>> c=CacheWithTimeLimit()
        >>> c.set("key","value")
        >>> c.delete("key")
        >>> c._cache["key"]
        Traceback (most recent call last):
        ...
        KeyError: 'key'
        """
        del self._cache[key]

    def flush(self):
        """
        >>> c=CacheWithTimeLimit()
        >>> c.set("key1","value1")
        >>> c.set("key2","value2")
        >>> c.flush()
        >>> c.get("key1")
        Traceback (most recent call last):
        ...
        KeyError: 'key1'
        >>> c.get("key2")
        Traceback (most recent call last):
        ...
        KeyError: 'key2'
        """
        self._cache = {}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
