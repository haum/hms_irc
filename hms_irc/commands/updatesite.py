from hms_irc.compat import handle as handle_compat



def handle(*args, **kwargs):
    handle_compat(*args, **kwargs)