import sys
import os

from setuptools import setup, find_packages

VERSION = '0.0.1'
LONG_DESCRIPTION = \
    open(os.path.join("src","README.txt")).read() + \
    open(os.path.join("src","TODO.txt")).read()

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: Python Software Foundation License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Topic :: Software Development",
]

setup(
    name='pyXurrency',
    version=VERSION,
    description='A Python interface to the Xurrency API',
    long_description=LONG_DESCRIPTION,
    classifiers=classifiers,
    keywords=['currency',],
    author='Masahito(Nakamura Masato)',
    author_email='randomstep at gmail dot com',
    url='https://github.com/masahitojp/pyXurrency',
    zip_safe=False,
    install_requires=[],
    license='PSL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data = {'': ['buildout.cfg']},
    include_package_data=True,
    extras_require=dict(
        test=[
            "Nose",
            "minimock",
            "pep8",
        ],
    ),
    test_suite='nose.collector',
    tests_require=['Nose','minimock','pep8'],
)

