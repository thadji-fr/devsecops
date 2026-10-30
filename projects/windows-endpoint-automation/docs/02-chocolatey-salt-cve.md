# 02 — Chocolatey, Salt et remédiation des CVE

## Problématique

Une vulnérabilité liée à un logiciel tiers demande plus qu'une commande d'installation : il faut déterminer si la version présente est concernée, disposer d'une version corrigée, la distribuer et vérifier le résultat.

J'ai participé à l'évolution de paquets Chocolatey et au déploiement de leurs mises à jour via Salt. La contribution portait sur la maintenance des versions et l'exécution de corrections centralisées, pas sur le développement d'un scanner CVE.

## Cycle technique

1. **Qualification** : logiciel, version déployée, versions affectées et disponibilité du correctif.
2. **Packaging** : version du paquet, source binaire, arguments d'installation, intégrité et codes de retour.
3. **Validation** : test du paquet sur un poste représentatif.
4. **Orchestration** : déploiement de la version voulue vers les postes concernés par Salt.
5. **Contrôle** : retour Salt, version installée, redémarrage et vérification que la version corrigée est bien active.

Un paquet disponible dans le dépôt ne signifie pas qu'il est installé ; une commande Salt réussie ne prouve pas, à elle seule, qu'une CVE a été corrigée.

## Illustration publique

L'[état Salt de laboratoire](../salt/states/browser-update.sls) illustre la mise à niveau ciblée d'un navigateur public via Chocolatey. Il utilise des valeurs fournies par Pillar, sans dévoiler ni dépôt, ni version de production, ni ciblage de machines. Il est **fictif** et n'est pas extrait des états d'origine.

Aucun délai de réaction, volume de postes, politique de déploiement ou automatisation complète de la veille CVE n'est revendiqué. Le code présenté nécessite validation dans un laboratoire.
