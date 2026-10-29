# Règles de publication

Ce dépôt est une **édition publique indépendante**, rédigée à partir de retours d'expérience. Il ne contient pas de configuration de production brute.

## À exclure avant chaque commit

- Clés privées et publiques identifiantes, secrets, tokens, cookies, comptes et `.env` réels.
- IP privées de production, FQDN d'administration, sous-réseaux, tables de routage, règles de filtrage effectives.
- Versions exactes de composants exposés, historique précis des correctifs, fenêtres d'incident non corrigées.
- Inventaires détaillés : nombre de conteneurs, volumes, nom des machines, puissance, compteurs de sécurité, journaux et captures brutes.
- Policies IAM, chemins alternatifs de connexion et information permettant de contourner un contrôle d'accès.

## Méthode

1. Conserver les preuves brutes dans le dépôt **privé**, jamais dans ce dépôt public.
2. Réécrire des exemples **fictifs et testables** sans reprendre les valeurs des fichiers de production.
3. Employer les domaines `example.org` / `example.invalid` et les plages de documentation RFC 5737 si une IP d'exemple est vraiment nécessaire.
4. Expurger les captures **par masques opaques**, notamment les adresses, versions, métriques et identités, puis supprimer les métadonnées.
5. Relire le diff, les pièces jointes, les liens et lancer `python3 scripts/check-public.py`.
6. Préparer la première publication avec un **historique Git neuf**. Masquer un secret dans un nouveau commit ne le retire pas d'anciens commits.

**Important :** ce filtre réduit l'exposition d'informations, mais ne constitue pas une garantie de sécurité. Toute erreur d'exposition d'un secret exige une rotation.
