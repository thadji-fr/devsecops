# Retour d'expérience : alerte ZFS

Au cours de l'exploitation, j'ai rencontré une **alerte d'état dégradé sur un pool ZFS**. Le pool est ensuite revenu à un état en ligne, avec une indication d'erreur corrigée. Les applications n'étaient pas annoncées comme affectées dans l'alerte observée.

Je ne dispose pas ici d'un dossier public suffisamment complet pour affirmer la cause racine, la séquence exacte des actions ou un diagnostic matériel définitif.

## Ce que je retiens

- Une alerte `ONLINE` après correction ne dispense pas de regarder l'historique et l'état des disques.
- Il faut distinguer erreur récupérée, erreur persistante et perte réelle de données.
- Un miroir ou un pool redondant ne remplace pas une sauvegarde restaurable.
- Un bon rapport d'incident doit conserver les preuves, les actions exécutées et les tests de retour à la normale **dans un espace privé**.

Je préfère publier une synthèse sans identifiants, sorties de commandes ou série matérielle, plutôt qu'un faux rapport complet.
