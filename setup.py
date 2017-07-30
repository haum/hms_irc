from distutils.core import setup
from setuptools import find_packages

from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hms_irc',
    use_scm_version=True,
    packages=find_packages(),

    url='https://github.com/haum/hms_irc',
    license='MIT',

    author='Romain Porte (MicroJoe)',
    author_email='microjoe@microjoe.org',

    description='HAUM\'s IRC microservice',
    long_description=long_description,

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    setup_requires=[
        'setuptools_scm',
    ],

    install_requires=[
        'hms_base>=2.0,<3',
        'pika',
        'coloredlogs',
        'irc',
        'attrs>16,<17',
    ],

    tests_requires=[
        'pytest',
        'flake8',
    ],

    entry_points={
      'console_scripts': [
          'hms_irc = hms_irc.main:main',
          'hms_irc_debug = hms_irc.debug:main',
      ]
    },
)
