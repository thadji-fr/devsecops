# Stacks Docker Compose — reconstruction anonymisée de mon architecture

Ce dossier modélise des stacks **séparées**, comme celles relevées dans mon inventaire. Chacune est indépendante côté Compose, mais les conteneurs rejoignent le **même réseau externe** (`example-edge`). Ce réseau remplace le vrai nom utilisé en production.

```text
             VPS frontal (Nginx)
                 │          │
         Réseau Docker      Tunnel WireGuard
          example-edge      vers serveurs distants
           ├── CrowdSec       ├── Web → IP VPN:port (HTTP)
           ├── Guacamole      └── Mail/voix → IP VPN:port (Stream)
           ├── MariaDB
           ├── guacd
           └── Arcane ── socket Docker sur le VPS
```

| Projet | Ports hôte dans le modèle | Volumes essentiels |
|---|---|---|
| [Nginx](edge.compose.yaml) | Web, courrier TCP, voix TCP/UDP | `/config` RW |
| [CrowdSec](crowdsec.compose.yaml) | `8080`, `3000` sur adresse WireGuard (loopback par défaut dans `.env.example`) | `/var/log/nginx` **RO**, config/data RW |
| [Guacamole](guacamole.compose.yaml) | `8085`, `3306`, `4822` sur loopback | enregistrements RO/RW, DB RW, drive RW |
| [Arcane Manager](arcane.compose.yaml) | `3552` sur l'IP WireGuard du VPS (repli loopback uniquement pour les tests) | socket Docker RW, data RW, projets RW |
| [Arcane Agent Direct](arcane-agent.example.yaml) | `3553` sur l'IP WireGuard de chaque serveur distant (aucune IP par défaut) | socket Docker RW sur l'hôte distant, données agent |

### Trois notions différentes

- La publication sur **`127.0.0.1`** concerne le port **de l'hôte**. Cela n'empêche pas un conteneur membre de `example-edge` de joindre un autre conteneur par son **nom + port interne**.
- Une **IP WireGuard** en `host_ip` limite l'interface de publication Docker. Ce n'est pas une politique firewall, ni une protection contre un accès direct depuis un autre membre de `example-edge`.
- Les **bind mounts** persistent la configuration, mais ne remplacent pas une sauvegarde ni un test de restauration. En particulier, l'accès RW au socket Docker d'Arcane reste une capacité d'administration à très hauts privilèges.

### Cohérence des montages et des chemins

Le **même chemin fictif** `STACK_ROOT/swag/log/nginx` est utilisé par le conteneur Nginx (sous `/config`) et CrowdSec (monté RO sous `/var/log/nginx`). Dans mon audit, j'ai vérifié cette relation entre dossiers sans publier les chemins réels. Pour Guacamole, le modèle utilise un chemin d'enregistrements commun entre guacd (RW) et l'application (RO) ; ce point **n'a pas encore été vérifié sur la configuration réelle**.

### Arcane et le réseau WireGuard

Le manager tourne sur le VPS et publie son port sur **l'IP WireGuard de ce VPS** ; chaque agent Direct publie son port sur **l'IP WireGuard de son propre hôte**. Le manager contacte les agents sur leurs adresses VPN. Nginx reçoit le trafic HTTPS public et relaie l'interface du manager vers l'IP WireGuard du VPS. Ce dernier saut est **local au VPS** : il ne constitue pas un tunnel chiffré supplémentaire.

Dans `arcane.compose.yaml`, le repli `127.0.0.1` est réservé aux vérifications de Compose : pour représenter la production, renseigner explicitement `WG_BIND_IP` dans un environnement privé. Le fichier `arcane-agent.example.yaml` exige `WG_AGENT_BIND_IP`, `WG_MANAGER_IP` et `ARCANE_AGENT_TOKEN` ; il n'embarque aucune valeur de production. **Ne pas le déployer sans vérifier le pare-feu, le routage, les droits et les secrets.**

Un binding sur une adresse donnée **réduit l'exposition** mais ne démontre pas que seul le tunnel peut joindre le port : Docker peut permettre certains chemins de routage direct selon la configuration du bridge et de l'hôte. Il faut tester IPv4/IPv6, la portée réelle des ports, les accès directs et les règles de pare-feu.

### Authentik et Arcane

Arcane me permet de centraliser la gestion de plusieurs environnements Docker (conteneurs, projets Compose, réseaux, volumes, images, journaux et console). J'ai placé son accès Web derrière **Nginx avec Forward Auth**, et **Authentik décide des autorisations par politique**, réservées à mon compte selon ma configuration. Le fichier Compose **ne contient pas** les providers, secrets ou règles Authentik. Voir [le reverse proxy anonymisé](../nginx/arcane-authentik.subdomain.conf).

### Tests automatiques

Le workflow public vérifie maintenant les quatre déclarations via `docker compose config --quiet` **sans démarrer de conteneur**, avec de faux identifiants. Cela vérifie la résolution de Compose, pas l'état réel des services ni la sécurité des fichiers déployés.

### Validation sans déployer

Dans un environnement de test préparé (réseau externe et chemins présents), copier `.env.example` vers `.env`, renseigner les secrets **hors dépôt**, puis lancer pour chaque modèle :

```bash
docker compose --env-file .env -f edge.compose.yaml config --quiet
docker compose --env-file .env -f crowdsec.compose.yaml config --quiet
docker compose --env-file .env -f guacamole.compose.yaml config --quiet
docker compose --env-file .env -f arcane.compose.yaml config --quiet
```

**Ne pas lancer `up` avec ces fichiers sur k3.** Ces modèles n'incluent pas les secrets de l'interface CrowdSec, les règles firewall, l'initialisation SQL Guacamole, la configuration complète des mods SWAG ni les règles de protection d'origine Cloudflare. Les images `latest` reflètent des conventions d'images observées ; dans un environnement exploité, définir une stratégie de versions et de mises à jour testées.

Pour une reproduction **ligne par ligne** de mes vrais Compose, il faudrait comparer ces modèles aux fichiers privés en lecture seule et publier uniquement un diff approuvé — ce travail reste ouvert.
