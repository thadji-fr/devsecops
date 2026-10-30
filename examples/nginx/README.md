# Nginx — fragments structurés comme l'architecture exploitée

Les fichiers conservent **l'organisation Nginx de l'infrastructure observée**, mais remplacent les domaines, adresses privées et upstreams. Ce ne sont **pas des exports de `nginx -T`**. Les options non relevées (timeout, SSL, headers) sont des choix illustratifs à valider, et non une reproduction attestée.

| Fichier | Rôle |
|---|---|
| [`http.conf`](http.conf) | Backend local à Nginx via **DNS Docker + port interne** |
| [`remote-wireguard.subdomain.conf`](remote-wireguard.subdomain.conf) | Backend HTTP distant via **IP du tunnel + port** (adresse RFC 5737) |
| [`arcane-authentik.subdomain.conf`](arcane-authentik.subdomain.conf) | Interface d'administration contrôlée par **Forward Auth Authentik via Nginx** |
| [`stream.conf`](stream.conf) | Bloc `stream` unique dans `nginx.conf` qui charge `stream-confs/*.conf` |
| [`stream-confs/mail-relay.conf`](stream-confs/mail-relay.conf) | Relais TCP en **passthrough** vers la messagerie |
| [`stream-confs/voice-relay.conf`](stream-confs/voice-relay.conf) | Relais vocal **UDP + TCP** |

## Arborescence d'installation habituelle (dans le conteneur Nginx)

```text
/config/nginx/
├── nginx.conf                  # contient déjà stream {} dans l'installation étudiée
├── proxy-confs/
│   ├── monitoring.subdomain.conf
│   ├── remote-app.subdomain.conf
│   └── admin.subdomain.conf
└── stream-confs/
    ├── mail-relay.conf
    └── voice-relay.conf
```

Les fichiers `.subdomain.conf` sont chargés par l'include Nginx sous `http {}`, tandis que les fichiers Stream sont chargés par le bloc `stream {}` au niveau principal. **Ne pas créer de deuxième bloc `stream`** si le fichier principal en possède déjà un. Les certificats et includes `ssl.conf`, `resolver.conf`, `proxy.conf`, `authentik-server.conf` et `authentik-location.conf` appartiennent à cette installation Nginx : leurs versions et les éventuelles personnalisations doivent être contrôlées séparément.

## Limites et contrôles

1. Les destinations `192.0.2.10` sont **non routables pour ton VPN** : remplace-les dans un banc de test par les vraies adresses de ce banc, jamais dans ce dépôt public.
2. Les règles de protection d'origine Cloudflare, `real_ip` et les bouncers CrowdSec sont **hors extrait** : ne pas les considérer comme automatiquement installés par ces fichiers.
3. Authentik **gère la décision d'autorisation** ; Nginx applique le Forward Auth. Un accès direct au port Docker du backend pourrait contourner Nginx et doit être empêché/testé séparément.
4. Les directives `listen` et les ports publiés Docker doivent correspondre et être filtrés sur IPv4/IPv6.
5. Sur l'hôte concerné seulement, valider avec `docker exec swag nginx -t` avant toute opération de rechargement. **Ne jamais copier ces exemples sur une instance de production en activité sans revue.**

Sources techniques : [Image Nginx LinuxServer](https://docs.linuxserver.io/images/docker-swag/), [Exemple d'include Authentik pour Nginx](https://github.com/linuxserver/docker-swag/blob/master/root/defaults/nginx/authentik-server.conf.sample), [Nginx Stream](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html), [Authentik Forward Auth](https://docs.goauthentik.io/add-secure-apps/providers/proxy/forward_auth).
