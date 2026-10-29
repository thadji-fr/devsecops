# De Proxmox à Docker Compose : un choix d'exploitation

Avant l'organisation actuelle, j'utilisais **Proxmox VE**, avec des VM et des LXC pour séparer les applications. Le modèle fonctionnait, mais je voulais limiter les ressources consacrées aux systèmes invités et simplifier les déploiements sur des machines de capacités différentes.

J'ai donc réparti les rôles entre plusieurs serveurs Linux et privilégié **Docker Compose** pour une grande partie des services. Ce n'est pas une affirmation selon laquelle Docker est meilleur que Proxmox : ce sont deux approches avec des avantages différents.

## Ce qui a réellement changé

| Avec Proxmox | Avec Docker Compose |
|---|---|
| Administration d'environnements VM/LXC | Déploiements par stacks de conteneurs |
| Systèmes invités et isolation VM | Noyau partagé et isolation à contrôler |
| Stockage adapté à chaque VM/LXC | Volumes et bind mounts gérés explicitement |
| Cycle de vie des systèmes invités | Cycle de vie des images et Compose |

Le passage aux conteneurs ne supprime **ni la gestion des droits, ni les sauvegardes, ni les risques de panne d'hôte**. J'ai notamment dû être plus rigoureux sur les montages, les réseaux et les interfaces de gestion.

Les applications restent familières : Nginx conserve son rôle de proxy, CrowdSec sa logique de collecte et de remédiation. C'est surtout leur mode d'installation, leurs journaux et leurs accès réseau qui évoluent.

## Les compromis

- Un bind mount RW peut donner à un conteneur la possibilité de modifier des fichiers de l'hôte.
- Un socket Docker monté dans une application d'administration peut conférer des droits très élevés.
- Publier un port sur une adresse locale ne bloque pas les communications internes à un même réseau Docker.
- Un volume persistant ne vaut pas sauvegarde ; les bases demandent une stratégie de sauvegarde cohérente.

Cette architecture me convient mieux au quotidien. Je n'annonce **aucun gain chiffré** de RAM, d'euros ou de disponibilité sans mesures comparables.

→ [Réseaux et volumes Compose](compose.md) · [Stockage et résilience](../storage-reliability/README.md)
