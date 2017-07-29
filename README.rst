hms_irc — Extensible IRC microservice
=====================================

.. image:: https://travis-ci.org/haum/hms_irc.svg?branch=master
    :target: https://travis-ci.org/haum/hms_irc

.. image:: https://coveralls.io/repos/github/haum/hms_irc/badge.svg?branch=master
    :target: https://coveralls.io/github/haum/hms_irc?branch=master

This microservice uses the principle of *receivers* and *commands*. It will
react into the IRC channel using receivers when data arrives from the watched
AMQP topics, and will send data to AMQP topics upon specific user commands.

Functional graph
----------------

Here is a concise graph of current *receivers* and *commands* implemented:

.. image:: doc/functional_graph/hms_irc.png
    :alt: Functional graph

Using
-----

Create a Python 3 virtualenv and install software::

    $ virtualenv -ppython3 venv
    $ source venv/bin/activate
    (venv) $ pip install .

Then start the bot inside the virtual env::

    (venv) $ hms_irc

License
-------

This project is brought to you under MIT license. For further information,
please read the provided ``LICENSE`` file.
