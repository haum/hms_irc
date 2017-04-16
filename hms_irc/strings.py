
# This file contains all strings in French

MUST_BE_VOICED = "Papiers, s'vousplaît ! Tu n'es pas voiced mon ami..."
UNKNOWN_ARGUMENT = "Argument invalide"

# Spacestatus

SPACESTATUS_HELP = "Aide : !spacestatus pour voir si l’espace est ouvert, " \
                   "autres commandes : !spacestatus [{}]"

SPACESTATUS_OPEN = "L'espace est ouvert !"
SPACESTATUS_CLOSED = "L'espace est fermé !"
SPACESTATUS_SAME_STATE = " (ATTENTION: état inchangé)"

# SpaceAPI

SPACEAPI_OPEN = "L'espace est ouvert ici"
SPACEAPI_CLOSED = "L'espace est fermé ici"
SPACEAPI_BAD_SSL = "certificat TLS invalide"
SPACEAPI_BAD_HTTP_CODE = "réponse HTTP invalide"
SPACEAPI_GLOBAL_ERROR = "erreur globale"

# Twaum/Spacestatus integration

TWAUM_OPEN = "@tweet INFO : notre espace est tout ouvert, " \
             "n’hésitez pas à passer si vous le voulez/pouvez ! haum.org"

TWAUM_CLOSED = "@tweet Fin de session ! Jetez un œil à notre agenda sur " \
               "haum.org pour connaître les prochaines ou " \
               "surveillez notre fil twitter."

# Agenda

AGENDA_HELP = (
    "Pour ajouter un élément : !agenda add JJ/MM/YYYY (h)h:mm \"Lieu\" \"Titre\" Description",
    "Pour ajouter une séance : !agenda add_seance JJ/MM/YYYY (h)h:mm",
    "Pour modifier un élément, : !agenda modify id [titre|lieu|date|status] nouvelle valeur",
    "Pour supprimer un élément, : !agenda remove id",
)

# Toot

TOOT_PENDING = "Demande de toot envoyée !"
TOOT_USAGE = "usage: !toot contenu de mon toot"