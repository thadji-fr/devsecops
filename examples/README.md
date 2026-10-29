# Exemples génériques — laboratoire uniquement

Les fichiers de ce dossier sont **reconstruits et fictifs**, pas des exports de mon infrastructure. Ils illustrent des principes de configuration, pas une installation sécurisée ou prête à lancer.

## Docker Compose

- [SWAG / frontal de test](compose/edge.compose.yaml)
- [CrowdSec et volumes de journaux](compose/crowdsec.compose.yaml)
- [Arcane et socket Docker](compose/arcane.compose.yaml)
- [Guacamole et base de données](compose/guacamole.compose.yaml)
- [Variables fictives](compose/.env.example)

## Nginx

- [Reverse proxy HTTP de démonstration](nginx/http.conf)
- [Relais Stream TCP de démonstration](nginx/stream.conf)

Les exemples demandent encore des certificats, une politique réseau, une gestion des identifiants, des sauvegardes et des validations applicatives. **Ne pas les déployer tels quels sur un serveur exposé.**
