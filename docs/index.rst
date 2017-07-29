.. hms_irc documentation master file, created by
   sphinx-quickstart on Sat Jul 29 16:48:17 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

hms_irc — Extensible IRC microservice
=====================================


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   commands
   receivers

How it works
------------

This microservice uses the principle of *receivers* and *commands*. It will
react into the IRC channel using receivers when data arrives from the watched
AMQP topics, and will send data to AMQP topics upon specific user commands.

Here is a concise graph of current *receivers* and *commands* implemented:

.. image:: images/functional_graph/hms_irc.png
    :alt: Functional graph
    :target: _images/hms_irc.png

`Commands <commands.rst>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
