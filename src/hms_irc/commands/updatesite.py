"""Requests an update for the content of the HAUM's website.

.. todo::

    This code is currently using the ``hanle_compat`` function.
    We should define a new AMQP protocol for this feature and apply it here.


Command usage::

    !updatesite

"""

from hms_irc.compat import handle as handle_compat


def handle(*args, **kwargs):
    handle_compat(*args, **kwargs)
