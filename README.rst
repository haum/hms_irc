hms_irc, the HAUM’s IRC microservice
====================================

A microservice that follows routing keys on a RabbitMQ direct exchanger and
publish messages on IRC depending on the messages received.

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
please read the provided ``LICENSE.txt`` file.
