# Nginx, WireGuard et CrowdSec — ce qui est prouvé et ce qu'il reste à tester

Je documente ici **trois niveaux de preuve différents** pour mon architecture Linux multi-sites : des constats recueillis en exploitation, des tests reproductibles sur **un laboratoire isolé** et des validations de sécurité encore ouvertes. L'objectif n'est pas de transformer mon infrastructure privée en inventaire public.

## 1. Ce que j'ai réellement observé

Les contrôles suivants proviennent d'un inventaire réalisé sur le VPS frontal, **pas** d'un environnement simulé :

| Sujet | Résultat observé | Ce que cela ne prouve pas |
|---|---|---|
| Nginx | La configuration chargée a réussi `nginx -t`. Les blocs HTTP et Stream étaient présents. | Qu'un client puisse joindre chaque backend ni que les règles de filtrage soient correctes. |
| Relais TCP/UDP | Des fichiers de relais de messagerie et de trafic vocal existaient, avec des directives `listen`, `upstream` et `proxy_pass`. | Que chaque port ou protocole fonctionne de bout en bout. |
| WireGuard | Des handshakes récents ont été constatés sur le hub. | Que les routes et règles inter-hôtes imposent réellement la politique souhaitée. |
| Docker | Nginx communique avec les services locaux par DNS Docker ; les backends distants sont configurés avec leur adresse WireGuard et leur port applicatif. | Que l'accès au port de l'hôte soit nécessaire, ni qu'un réseau Docker partagé fournisse de l'isolation latérale. |
| Journaux Nginx → CrowdSec | Comparaison locale confirmant que le montage en lecture seule de CrowdSec pointe sur le sous-dossier `log/nginx` du volume Nginx. | Que chaque type d'événement soit correctement parsé. |
| CrowdSec | Des métriques de collecte, alertes d'un agent distant et rejets côté Nginx/pare-feu ont été relevés. | Que toutes les décisions ou tous les bouncers fonctionnent à cet instant. |

### Vérification complémentaire de la configuration chargée — 30 octobre 2026

Un contrôle **en lecture seule** avec `nginx -T` sur le conteneur de frontal a confirmé que l'ensemble de la configuration était accepté par Nginx. Les fichiers de proxy HTTP et de relais Stream ont été détectés, ainsi que les directives d'écoute correspondant aux protocoles documentés. Le script de comparaison utilisé n'a pas signalé d'écoute supplémentaire dans son périmètre d'analyse.

Le même relevé détecte des références à **Authentik, CrowdSec, Real IP et PROXY protocol** dans les fichiers chargés. Cela établit leur **présence structurelle**, pas leur efficacité ni leur placement exact sur les routes. En particulier, l'usage de **PROXY protocol sur le relais SMTP** n'a pas encore été déterminé. Les nombreuses directives `proxy_pass` à variables ne doivent pas être interprétées comme autant de services indépendants.

Pour approfondir ce point sans afficher les valeurs sensibles, j'ai ajouté le script [`scripts/audit-nginx-flags-safe.py`](../../scripts/audit-nginx-flags-safe.py). Il inspecte `nginx -T` en mémoire et n'imprime que des indicateurs prédéfinis `OUI`, `NON` ou `INDÉTERMINÉ`. Il ne vérifie pas la pertinence des règles d'accès et n'effectue aucune requête réseau vers les backends.

Les captures d'écran brutes, IP WireGuard, compteurs détaillés, adresses d'administration et chemins sources restent **hors du dépôt public**.

## 2. Tests reproductibles sur les exemples PUBLICS

La validation automatisée du dépôt comporte désormais :

1. **Analyse de sécurité documentaire** des textes avec `scripts/check-public.py` (heuristique, pas garantie absolue).
2. **Lecture YAML** des exemples, et contrôle des montages, réseaux et ports entre Compose et Nginx Stream.
3. **Résolution des vrais modèles Compose** via `docker compose config --quiet`, avec des identifiants de laboratoire factices. Cela ne démarre aucun conteneur.
4. **`nginx -t` sur les fragments du dépôt**, chargés dans une configuration temporaire. Les certificats sont autosignés et les includes absents sont remplacés **uniquement pendant le test** par des doublures clairement identifiées.
5. **Tests de chemin HTTP(S), TCP et UDP en local**, via des backends simulés en `127.0.0.1` et des ports élevés. Les scripts substituent temporairement les adresses réservées à la documentation ; les fichiers du dépôt ne sont pas réécrits.

**Premier résultat GitHub Actions vérifié (30 octobre 2026) :** la résolution des Compose, `nginx -t` et les tests de chemin HTTP(S), TCP et UDP de laboratoire ont tous réussi. [Voir l'exécution et ses journaux](https://github.com/thadji-fr/devsecops/actions/runs/41027757756). Un succès de CI porte sur les **exemples reconstruits**, pas sur l'accessibilité des services réels ni sur les politiques de sécurité du VPS.

Le script principal se lance sur un hôte de test avec Nginx, OpenSSL et le module Stream :

```bash
python3 scripts/test-nginx-examples.py --smoke
```

Pour valider seulement les fragments HTTP lorsque le module Stream n'est pas installé :

```bash
python3 scripts/test-nginx-examples.py --http-only
```

**Limite majeure :** la doublure Authentik renvoie volontairement une réponse favorable pour vérifier seulement la **syntaxe et l'acheminement** ; elle **ne valide ni OIDC, ni Forward Auth, ni les permissions Authentik**. Le certificat temporaire ne prouve rien sur le TLS public. Ces tests ne sollicitent pas les serveurs on-premises.

## 3. Tests de production encore nécessaires, sans publier les détails

| Cas | Méthode attendue | Preuve publique possible | État |
|---|---|---|---|
| Parcours client → Nginx → service HTTP distant | Test depuis un client autorisé avec réponse applicative connue | Résultat positif/négatif anonymisé | À confirmer |
| Relais TCP messagerie | Vérifier d'abord la direction de PROXY protocol (entrant/sortant) sur le relais SMTP, puis la négociation sur un service autorisé | Résultat anonymisé, sans noms d'hôte ni IP | Structure en cours d'audit ; chemin complet à confirmer |
| Relais UDP vocal | Test UDP adapté au protocole avec un client prévu à cet effet | Succès/échec, sans endpoints | À confirmer |
| Politique réseau WireGuard | Essais autorisés puis refusés entre hôtes, et vérification des règles sur les deux extrémités | Matrice de résultats sans règles ni adresses | À confirmer |
| Accès direct à l'origine / IPv6 | Essais depuis un réseau externe contrôlé, pour vérifier le refus de contournement du frontal | Résultat du test et remédiation | À confirmer |
| Véritable IP client / Cloudflare | Vérifier la chaîne de confiance `real_ip` et les logs, sans imprimer l'IP | Preuve anonymisée | À confirmer |
| CrowdSec de bout en bout | Déclencher un événement **autorisé en environnement de test**, observer son analyse et une décision appliquée | État par étape, sans IP ni secret | À confirmer |
| Authentik et outil d'administration | Comparer visiteur anonyme, utilisateur non autorisé et compte autorisé ; essayer aussi le backend direct | Matrice autorisé/refusé | À confirmer |

## 4. Captures à joindre au portfolio

Sur les pages des projets et dans les articles de [thadji.fr](https://thadji.fr), privilégier des **captures réelles mais expurgées** : sortie courte de `nginx -t`, test HTTP d'un service de laboratoire, état d'un relais TCP/UDP de test et résultat global de collecte CrowdSec. La légende doit distinguer **laboratoire** et **production**. Masquer de façon opaque domaines privés, IP, ports d'administration, comptes et identifiants ; éviter de publier les règles effectives de sécurité.

L'automatisation ci-dessus améliore la confiance dans les **exemples publics**. Elle ne remplace pas l'audit de la configuration Nginx réelle ni la démonstration que les protections du VPS sont efficaces.