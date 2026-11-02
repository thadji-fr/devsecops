# Nginx — fragments structurés comme l'architecture exploitée

Les fichiers conservent **l'organisation Nginx de l'infrastructure observée**, mais remplacent les domaines, adresses privées et upstreams. Ce ne sont **pas des exports de `nginx -T`**. Les options non relevées (timeout, SSL, headers) sont des choix illustratifs à valider, et non une reproduction attestée.

| Fichier | Rôle |
|---|---|
| [`http.conf`](http.conf) | Backend local à Nginx via **DNS Docker + port interne** |
| [`remote-wireguard.subdomain.conf`](remote-wireguard.subdomain.conf) | Backend HTTP distant via **IP du tunnel + port** (adresse RFC 5737) |
| [`arcane-authentik.subdomain.conf`](arcane-authentik.subdomain.conf) | Interface d'administration contrôlée par **Forward Auth Authentik via Nginx** |
| [`stream.conf`](stream.conf) | Bloc `stream` unique dans `nginx.conf` qui charge `stream-confs/*.conf` |
| [`stream-confs/mail-relay.conf`](stream-confs/mail-relay.conf) | Relais TCP en **passthrough** vers la messagerie ; **en-tête PROXY protocol émis vers l'écoute Postscreen compatible** dans l'exemple |
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

## Tests de syntaxe et de circulation (laboratoire)

Les fragments de ce dossier sont assemblés **sans les modifier dans Git** dans un répertoire temporaire, avec un certificat autosigné et des includes de test. Puis la CI lance `nginx -t` et un test de chemin **HTTP(S), TCP et UDP**, avec des backends émulés en `127.0.0.1`. La configuration de test remplace dans les copies temporaires les adresses d'exemple et les ports pour éviter tout accès à une machine réelle.

```bash
python3 scripts/test-nginx-examples.py --smoke
```

Le script est lancé depuis la racine du dépôt avec Nginx, OpenSSL et le module Nginx Stream installés. Pour une vérification syntaxique HTTP seule : `python3 scripts/test-nginx-examples.py --http-only`.

**Attention : les includes Authentik du laboratoire sont des doublures.** Leur réponse favorable ne teste ni la véritable authentification, ni les permissions, ni un contournement possible du backend. Les certificats ne valident pas TLS en production, et ces tests ne touchent pas WireGuard.

→ [Matrice des preuves réelles et des contrôles encore ouverts](../../projects/network-edge/validation.md).

## Audit passif de la configuration réelle

Pour comparer les *familles de directives chargées* à celles des exemples, je peux exécuter le script [`audit-nginx-flags-safe.py`](../../scripts/audit-nginx-flags-safe.py) **sur le serveur concerné**. Il récupère la sortie de `nginx -T` en mémoire, sans la publier, et imprime uniquement une liste fermée de `OUI`/`NON`/`INDÉTERMINÉ`.

```bash
python3 scripts/audit-nginx-flags-safe.py
```

Le relevé en lecture seule a confirmé **PROXY protocol en sortie du relais SMTP**, mais **pas en entrée depuis les clients**. Les paramètres de service du serveur de messagerie confirment des écoutes Postfix dédiées compatibles ; **la liaison effective Nginx → écoute Mailcow n'est pas encore vérifiée**. L'exemple Nginx reflète désormais cette directive. En laboratoire, le backend simulé vérifie qu'il reçoit l'en-tête PROXY v1 avant les données TCP. L'audit distingue aussi **PROXY protocol entrant** (`listen ... proxy_protocol`) et **sortant** (`proxy_protocol on;`) pour les autres fichiers Stream. Cela **ne prouve pas** que le backend accepte PROXY protocol. La lecture est strictement passive, sans rechargement ni modification de service. Contrôler le script avant son exécution.

## Vérifier localement le port de destination Nginx → Mailcow

L'audit passif complémentaire [`audit-nginx-mailcow-routes-safe.py`](../../scripts/audit-nginx-mailcow-routes-safe.py) analyse les *upstreams* et les directives `listen` dans les fichiers Stream chargés. Les seules valeurs affichées sont des indicateurs `OUI` / `NON` / `INDÉTERMINÉ` pour les ports dédiés SMTP, SMTPS et Submission et la présence d'une directive PROXY protocol.

```bash
python3 scripts/audit-nginx-mailcow-routes-safe.py
```

Il faut le lancer **sur le frontal Nginx**, pas sur le serveur Postfix. Le script ne modifie aucun fichier ni service. Il ne sait pas reconstituer une éventuelle redirection de port par Docker ou un relais intermédiaire. `NON` ne constitue donc pas, seul, une preuve de panne ou une justification de modification en production.

## CrowdSec, Cloudflare et l'IP réelle des visiteurs

L'article [**CrowdSec et Nginx : détecter et bloquer les attaques Web**](https://thadji.fr/crowdsec-nginx-swag-npm/) est documenté côté dépôt dans [**l'étude de cas Nginx / CrowdSec**](../../projects/crowdsec/nginx-reverse-proxy.md).

Cette installation s'appuie sur **Nginx** ; SWAG n'est que l'image Docker Nginx utilisée (certificats automatiques et modules complémentaires). Le nom `swag` dans les commandes est le nom de ce conteneur.

La configuration publique de ce dossier **n'intègre pas les réglages du bouncer Lua ni la liste de confiance Cloudflare** : cela ne signifie pas que CrowdSec est installé ou que les IP clientes sont restaurées par ces fragments. En exploitation, la confiance accordée à `CF-Connecting-IP` doit être limitée aux plages Cloudflare officielles, pour les flux qui arrivent effectivement depuis leurs relais.

Pour les domaines Cloudflare proxifiés, un bouncer HTTP intégré à Nginx peut utiliser l'IP visiteur restaurée ; un bouncer firewall sur l'hôte traite les **IP sources réseau** observables (généralement celles des relais Cloudflare pour ces flux). Les sites DNS-only et les services TCP/UDP sont à vérifier sur leur propre chemin réseau.

Un `nginx -t` réussi ou la présence de directives CrowdSec dans `nginx -T` ne démontrent pas un bannissement HTTP réel. Une preuve de remédiation exige un test depuis un client contrôlé, avec décision temporaire, observation de la réponse et nettoyage du test.

## Limites et contrôles

1. Les destinations `192.0.2.10` sont **non routables pour ton VPN** : remplace-les dans un banc de test par les vraies adresses de ce banc, jamais dans ce dépôt public.
2. Les règles de protection d'origine Cloudflare, `real_ip` et les bouncers CrowdSec sont **hors extrait** : ne pas les considérer comme automatiquement installés par ces fichiers.
3. Authentik **gère la décision d'autorisation** ; Nginx applique le Forward Auth. Un accès direct au port Docker du backend pourrait contourner Nginx et doit être empêché/testé séparément.
4. Les directives `listen` et les ports publiés Docker doivent correspondre et être filtrés sur IPv4/IPv6.
5. Sur l'hôte concerné seulement, valider avec `docker exec swag nginx -t` avant toute opération de rechargement. **Ne jamais copier ces exemples sur une instance de production en activité sans revue.**

Sources techniques : [Image Nginx LinuxServer](https://docs.linuxserver.io/images/docker-swag/), [Exemple d'include Authentik pour Nginx](https://github.com/linuxserver/docker-swag/blob/master/root/defaults/nginx/authentik-server.conf.sample), [Nginx Stream](https://nginx.org/en/docs/stream/ngx_stream_proxy_module.html), [Authentik Forward Auth](https://docs.goauthentik.io/add-secure-apps/providers/proxy/forward_auth).
