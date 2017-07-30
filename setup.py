from setuptools import find_packages, setup

import os
import sys

base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the src/ directory to the sys.path.
sys.path.insert(0, src_dir)

# Use README as long description
with open(os.path.join(base_dir, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='hms_irc',
    use_scm_version=True,

    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=['tests', 'tests.*']),

    url='https://github.com/haum/hms_irc',
    bugtrack_url='https://github.com/haum/hms_irc/issues',
    license='MIT',
    platforms='any',

    author='Romain Porte (MicroJoe)',
    author_email='microjoe@microjoe.org',

    description='Extensible IRC microservice',
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
