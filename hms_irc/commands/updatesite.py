"""Requests an update for the content of the HAUM's website.

.. todo::

    This code is currently using the ``CompatIRCHandler`` class.
    We should define a new AMQP protocol for this feature and apply it here.


Command usage::

    !updatesite

"""

from hms_irc.irc.handlers import CompatIRCHandler


def get_instance(*args):
    return CompatIRCHandler(*args)
