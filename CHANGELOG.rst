Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

[Unreleased]
------------

- Added Sphinx documentation
- Cleaned code using flake8
- Enforce flake8 for new commits on CI

[2.5] - 2017-07-29
------------------

- Added support for spacestatus toggle command
- Reworked README and overall documentation
- Using SCM version and entrypoints for setup.py

[2.4] - 2017-05-08
------------------

- Added more tests and refactored code in order to to enhance contribution
  experience
- Automatic reconnect attempt every hour
- Allow manual reconnect attempt using SIGUSR1

[2.3] - 2017-04-16
------------------

- Allow users to send toots directly for ``hms_mastodon``

[2.2] - 2017-04-04
------------------

- Added IRC command support for spacestatus microservice
- All the IRC part can and should now be handled by the IRC microservice and not
  by the microservices themselves (backward compatibility available)
- Send ``is_voiced`` information when a command is performed
- Refactored all the code into transmitters/receivers system using introspection

[2.1] - 2016-08-15
------------------

- Using ``hms_base`` version 2

[2.0] - 2016-06-19
------------------

- Using package ``hms_base`` instead of copying its source code
- Using ``setup.py`` packaging for easier installation, dependency management
  and use

[1.1] - 2016-05-24
------------------

- Global ping/pong handling over IRC
- Using generic RabbitMQ wrapper for easy reuse
- Removed kicked-user-made-bot-think-he-was-kicked bug

[1.0] - 2016-04-14
------------------

- First prototype
