# Administration systèmes Linux, réseau et sécurité

[![Tests des exemples](https://github.com/thadji-fr/devsecops/actions/workflows/public-check.yml/badge.svg)](https://github.com/thadji-fr/devsecops/actions/workflows/public-check.yml)

Je suis administrateur systèmes et je documente ici des configurations que j'ai utilisées, des problèmes rencontrés et les solutions retenues. Mes projets portent principalement sur **Linux, les réseaux, Docker et la sécurisation des accès**, avec aussi des travaux d'automatisation Windows.

Aujourd'hui, mon architecture repose sur un **VPS Debian en frontal** et plusieurs serveurs Linux accessibles par **WireGuard**. Le VPS reçoit les connexions publiques ; les services hébergés sur les autres serveurs ne nécessitent pas de redirection de ports sur leurs routeurs.

Ce dépôt est le prolongement technique des articles de [thadji.fr](https://thadji.fr/). J'y conserve des exemples de configuration, des scripts de vérification et des notes d'exploitation, avec les informations sensibles retirées.

## Les projets

### Réseau et exposition des services

Mon VPS sert de point d'entrée pour des services répartis sur plusieurs serveurs. **Nginx** gère les requêtes HTTP(S), tandis que son module **Stream** relaie certains flux TCP et UDP, notamment pour la messagerie et les services vocaux. Les backends distants sont joints par WireGuard.

- [Architecture du VPS frontal](projects/network-edge/README.md)
- [WireGuard entre VPS et serveur Linux privé](projects/network-edge/wireguard-vps-onprem.md)
- [Relais TCP/UDP avec Nginx Stream](projects/network-edge/nginx-stream-wireguard.md)
- [Exemples de configuration Nginx](examples/nginx/README.md)

### Sécurité et contrôle des accès

J'utilise **CrowdSec** pour analyser des événements et centraliser les décisions de sécurité. Selon le trafic concerné, les décisions peuvent être appliquées par Nginx ou par un bouncer firewall. Pour les interfaces d'administration, j'utilise également **Authentik** avec OIDC ou Forward Auth.

- [CrowdSec : agents, LAPI et remédiation](projects/crowdsec/README.md)
- [CrowdSec avec Nginx et Cloudflare](projects/crowdsec/nginx-reverse-proxy.md)
- [Supervision avec CrowdSec Web UI](projects/crowdsec/web-ui.md)
- [Authentik et gestion des accès](projects/identity-access/README.md)

### Conteneurs et exploitation Linux

J'administre plusieurs environnements Docker. J'ai notamment travaillé sur leur centralisation avec **Arcane**, la gestion des volumes et les migrations de services. Mes notes couvrent aussi un incident sur un pool **ZFS** et les contrôles réalisés après sa remise en état.

- [Administration Docker avec Arcane](projects/docker-management/README.md)
- [Plateforme Docker et migration](projects/docker-platform/README.md)
- [Stockage ZFS et retour d'incident](projects/storage-reliability/README.md)

### Déploiement et administration Windows

J'ai participé à la **maintenance d'une chaîne de déploiement Windows existante** : PXE, fichiers Unattended, scripts Batch/PowerShell, dépôt Chocolatey interne et préparation des postes. J'ai également utilisé **Salt** pour l'administration distante et les interventions sur plusieurs machines.

Les exemples publics ont été reconstruits avec des noms et paramètres fictifs ; ils ne contiennent pas les logiciels ou les configurations internes d'origine.

- [Déploiement Windows : PXE et Unattended](projects/windows-endpoint-automation/docs/01-pxe-windows.md)
- [Administration distante avec Salt et Chocolatey](projects/windows-endpoint-automation/docs/02-salt-chocolatey-administration.md)
- [Création d'un paquet Chocolatey MSI](projects/windows-endpoint-automation/docs/03-chocolatey-custom-package.md)

J'ai aussi documenté une [ancienne architecture Proxmox + OPNsense sur OVHcloud](projects/proxmox-opnsense-historical/README.md). Elle ne correspond plus à mon infrastructure actuelle.

## Exemples et vérifications

Ce dépôt **n'est pas une sauvegarde de mes serveurs** : les adresses, domaines, identifiants et éléments sensibles sont absents ou remplacés. Les fichiers publics sont des exemples à étudier et à adapter, pas des configurations à appliquer directement en production.

Il y a néanmoins du code vérifiable :

- [Configurations Docker Compose](examples/compose/README.md) et [fragments Nginx](examples/nginx/README.md) anonymisés ;
- [Tests locaux Nginx HTTP(S), TCP et UDP](scripts/test-nginx-examples.py) avec des backends simulés ;
- [Script d'audit passif Nginx](scripts/audit-nginx-flags-safe.py), conçu pour ne pas imprimer les directives sensibles ;
- [GitHub Actions](.github/workflows/public-check.yml) pour contrôler les exemples et exécuter les tests de laboratoire.

J'ai aussi rédigé une [synthèse des contrôles effectués et des tests qui restent à faire](projects/network-edge/validation.md). Une configuration valide avec `nginx -t` ou un handshake WireGuard ne suffisent pas à démontrer qu'un service est accessible — ou correctement isolé.

---

Pour retrouver tous les dossiers : [projets](projects/README.md) · [exemples](examples/README.md) · [articles sur thadji.fr](https://thadji.fr/).
