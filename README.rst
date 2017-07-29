hms_irc — Extensible IRC microservice
=====================================

.. image:: https://travis-ci.org/haum/hms_irc.svg?branch=master
    :target: https://travis-ci.org/haum/hms_irc

.. image:: https://coveralls.io/repos/github/haum/hms_irc/badge.svg?branch=master
    :target: https://coveralls.io/github/haum/hms_irc?branch=master

.. image:: https://readthedocs.org/projects/hms-irc/badge/?version=latest
    :target: http://hms-irc.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

AMQP-based microservice for bidirectionnal IRC interactions.

Service responsabilities:

- Deliver information to users on IRC upon AMQP broadcasts on interesting topics
- Verify and help users in building AMQP messages for other microservices
- Allow users and other microservices to communicate using commands/responses

hms_irc is part of the `HAUM Micro-Services (HMS)`_ tools.

.. _HAUM Micro-Services (HMS): https://github.com/haum/hms

Quick start
-----------

Create a Python 3 virtualenv and install software::

    $ virtualenv -ppython3 venv
    $ source venv/bin/activate
    (venv) $ pip install .

Then start the bot inside the virtualenv::

    (venv) $ hms_irc

You can send arbitrary IRC messages using the provided debug tool::

    (venv) $ hms_irc_debug hello world


License
-------

This project is brought to you under MIT license. For further information,
please read the provided ``LICENSE`` file.
