# Salt — orchestration documentaire

La [définition d'état](states/browser-update.sls) représente une mise à niveau de navigateur avec le module Salt Chocolatey. Il s'agit d'un exemple **fictif**, non extrait de la configuration Salt d'origine.

L'état utilise `chocolatey.upgraded` et reçoit la version corrigée ainsi que l'adresse du dépôt par Pillar. Ces paramètres doivent être renseignés dans un laboratoire et testés avec les versions exactes de Salt et Chocolatey.

Le ciblage des machines, le traitement des retours, la gestion des redémarrages et les règles de remédiation CVE ne sont **pas implémentés** dans cet exemple.
