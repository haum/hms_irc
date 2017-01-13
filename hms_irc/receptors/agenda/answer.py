import time


def handle(irc_server, irc_chan, dct):

    def irc(msg):
        irc_server.privmsg(irc_chan, msg)

    def testkey(key):
        return key in dct and dct[key]

    # Ignore answers with a source that is not IRC
    if not 'source' in dct or dct['source'] != 'irc':
        return

    if 'list' in dct:
        if dct['list']:
            for event in dct['list']:
                irc('#{0}: {1} ; {2} le {4} {5}'.format(*event))
                time.sleep(1) # avoid spamming too fast
        else:
            irc('Aucun événement prochainement')

    if testkey('remove'):
        irc('Événement correctement supprimé')
    if testkey('add'):
        irc('Événement ajouté !')
    if testkey('add_seance'):
        irc('Séance ajoutée !')
    if testkey('modify'):
        irc('Modification effectuée !')