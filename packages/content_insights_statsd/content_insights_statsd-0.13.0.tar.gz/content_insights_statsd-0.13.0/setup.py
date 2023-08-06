import codecs
import os

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


long_des = read("README.rst")

platforms = ['linux/Windows']
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]


setup(name='content_insights_statsd',
      version='0.13.0',
      description='A test module for statsd in airflow operator',
      long_description=long_des,
      py_modules=['content_insights_statsd.bash_operator','content_insights_statsd.python_operator','content_insights_statsd.prom_statsd'],
      author="myang",
      author_email="407768752@qq.com",
      license="Apache License, Version 2.0",
      platforms=platforms,
      classifiers=classifiers
      )
