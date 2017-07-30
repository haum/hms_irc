"""These modules are triggered depending on the received AMQP topic.

Listenning to a new topic
-------------------------

If you want to listen to a new AMQP topic, you have to create a Python module
that matches the topic name and implement a ``handle`` function in this module
with the following signature::

    def handle(irc_server, irc_chan, dct):
        pass

For example, if you want to listen to the ``agenda.broadcast`` topic, you will
have to create the following architecture::

    agenda
    ├── broadcast.py
    └── __init__.py

    0 directories, 2 files

And then you have to declare and implement the ``handle`` function in the
``broadcast.py`` file.

.. warning::

    You will also have to add your topic into the ``RABBIT_ROUTING_KEYS`` set
    inside the ``settings.py`` file if not already matched. Note that if
    ``agenda.*`` is defined in this set then there is no need to append a
    ``agenda.broadcast`` rule.

"""
