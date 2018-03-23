from hms_irc.irc.exceptions import NotVoicedError


def voiced(handler):
    """Verify that the passed command is voiced before calling method.

    If the user that calls the command is not voiced, this decorator
    will raise a NotVoicedError.

    """
    def verify_voiced(instance, command):
        if not command.is_voiced:
            raise NotVoicedError

        handler(instance, command)
    return verify_voiced
