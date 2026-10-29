# Arcane : piloter mes environnements Docker depuis une seule interface

J'ai fini par déployer **Arcane** pour gagner du temps dans l'administration quotidienne. Plutôt que d'ouvrir une session sur chaque serveur à chaque vérification, j'utilise une **interface centrale** pour retrouver les environnements et effectuer les opérations courantes.

J'y retrouve notamment la gestion des **conteneurs**, des projets **Docker Compose**, des **images**, des **réseaux**, des **volumes**, les **journaux**, une **console** et les **mises à jour**. Les environnements distants remontent via des agents. C'est une centralisation de l'administration, pas la disparition des contrôles de sécurité de chaque serveur.

> Une capture réelle de l’interface a été conservée en privé. Elle sera ajoutée ici après une validation finale de son anonymisation : je préfère éviter de publier les chiffres opérationnels et les détails des environnements.


## Sécurité

J'ai déclaré **Authentik (OIDC et Forward Auth via SWAG)** avec des permissions limitées au compte autorisé. La protection des comptes et des accès réseau ne retire pas la sensibilité d'une interface capable d'agir sur les conteneurs.

Un gestionnaire qui possède l'accès au **socket Docker** détient potentiellement des capacités élevées sur l'hôte : il faut maîtriser le chemin réseau, les droits, les mises à jour, l'audit et les accès de contournement.

Je ne publie ni les adresses des agents ni les politiques d'Authentik. Les tests d'authentification et de non-contournement doivent être réalisés sur l'environnement réel, sans en diffuser les détails.

→ [Compose Arcane anonymisé](../../examples/compose/arcane.compose.yaml) · [Forward Auth SWAG anonymisé](../../examples/nginx/arcane-authentik.subdomain.conf) · [Retour d'expérience Compose](../docker-platform/compose.md) · [Authentik et Forward Auth](../identity-access/README.md)
