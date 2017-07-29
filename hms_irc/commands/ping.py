"""Sends ping to all services.

.. todo::

    This code is currently using the ``hanle_compat`` function.
    We should define a new AMQP protocol for this feature and apply it here.

"""

from hms_irc.compat import handle as handle_compat


def handle(*args, **kwargs):
    handle_compat(*args, **kwargs)
