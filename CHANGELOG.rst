Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

[Unreleased]
------------

- Added IRC command support for spacestatus microservice
- All the IRC part can and should now be handled by the IRC microservice and not
  by the microservices themselves (backward compatibility available)
- Send ``is_voiced`` information when a command is performed

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
