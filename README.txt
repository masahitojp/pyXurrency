This package implements an interface to the Xurrency API, defined at http://xurrency.com/api.

Requirements
------------
* Python 2.6 or later (not support 3.x)

Features
--------
* Currency convert

Setup
-----
::

   $ easy_install pyXurrency

or from the source::
	
    ./setup.py develop

Usage
-----

::

    >>> from xurrency import Xurrency
    >>> xapi = Xurrency()
    >>> xapi.get_rate('eur', 'gbp', 1.5)
    1.3014

or You have License Key  ::

    >>> LICENSE_KEY = "foobar"
    >>> xapi_with_key = Xurrency(LICENSE_KEY)


History
-------

0.0.1 (2011-03-01)
~~~~~~~~~~~~~~~~~~
* first release

