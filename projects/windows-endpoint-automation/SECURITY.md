# Sécurité, provenance et limites de publication

Les fichiers publiés sont **des reconstructions documentaires anonymisées**. Les sources d'origine ne sont pas distribuées.

## Exclusions systématiques

- Binaires MSI, archives NUPKG, fichiers de production et scripts récupérés tels quels.
- Adresses IP et noms d'hôtes, chemins UNC, noms de domaine, identifiants et informations propres à un parc.
- Paramètres d'authentification, mots de passe et configurations internes susceptibles de figurer dans les scripts et installateurs d'origine.
- Copies de configurations PXE/Salt non examinées ou appartenant à des tiers.

## Mesures attendues

- Contrôler droits de redistribution, signatures et SHA-256 de tout installateur.
- Ne jamais injecter de secret dans un paquet Chocolatey ni le passer en clair dans un argument de processus observable.
- Vérifier les codes retour, redémarrages et versions réellement installées.
- Tester les reconstructions sur un laboratoire isolé avant de les réutiliser.
- Retirer des captures les données de postes, d'utilisateurs, de serveur ou de réseau.

Si les identifiants détectés dans les archives originales sont toujours utilisés, ils doivent être renouvelés. Ces exemples ne constituent pas une preuve de validation en production.
