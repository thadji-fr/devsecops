# Exemples de configuration basés sur mon architecture

Je publie ici des **reconstructions anonymisées de la structure que j'exploite**, et non de petits extraits indépendants recopiés d'un tutoriel.

Le **périmètre technique** est fondé sur mes inventaires : frontal Nginx, relais mail/vocal dans Nginx Stream, CrowdSec LAPI + Web UI, Guacamole/MariaDB/guacd, Arcane + socket Docker, **un réseau externe partagé** et des services distants joints par WireGuard. Les paramètres applicatifs impossibles à vérifier sans lire mes fichiers réels ne sont **pas présentés comme exacts**.

## Configuration détaillée

- [Mode d'emploi, topologie et limites des Compose](compose/README.md)
- [Nginx — frontal HTTP(S) et Stream TCP/UDP](compose/edge.compose.yaml)
- [CrowdSec — LAPI, interface Web et logs Nginx RO](compose/crowdsec.compose.yaml)
- [Guacamole — application, MariaDB et guacd](compose/guacamole.compose.yaml)
- [Arcane — manager Docker, socket et projets Compose](compose/arcane.compose.yaml)
- [Variables fictives pour un laboratoire](compose/.env.example)
- [Nginx : reverse proxies HTTP, Authentik et Stream](nginx/README.md)
- [CrowdSec : acquisition de logs Nginx](crowdsec/acquis.d/nginx.yaml)

**Sécurité :** les fichiers ne contiennent pas de secrets, clés, adresses de pairs VPN, domaines d'administration, politiques IAM ni versions détaillées de production. Ils documentent les choix techniques, **pas une configuration prête à démarrer sur Internet**.
