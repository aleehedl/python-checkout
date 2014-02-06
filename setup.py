"""
checkout
============

Python wrapper for the Checkout Finland API.

Links
-----

* `documentation <http://packages.python.org/checkout>`_
* `development version
  <http://github.com/tuomasb/python-checkout/zipball/master#egg=checkout-dev>`_

"""
import os
import re

from setuptools import setup


HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'checkout', '__init__.py')
    contents = open(filename).read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


setup(
    name='checkout',
    version=get_version(),
    description='Python wrapper for the Checkout Finland API.',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    author='Tuomas Blomqvist, Janne Vanhala',
    author_email='tuomas.blomqvist@gmail.com, janne@fastmonkeys.com',
    url='http://github.com/tuomasb/python-checkout',
    packages=['checkout'],
    include_package_data=True,
    license='BSD',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
