try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages 

VERSION = '0.0.1'
long_description = ''
classifiers = [
]

setup(
    name='pyXurrency',
    version=VERSION,
    description='',
    long_description=long_description,
    keywords=[],
    author='',
    author_email='',
    url='',
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

