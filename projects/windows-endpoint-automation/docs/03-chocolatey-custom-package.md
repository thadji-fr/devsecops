# 03 — Packaging Chocolatey : construire et maintenir un paquet MSI

**Étude de cas anonymisée** — Le logiciel d'origine, sa version et les informations du système destinataire ne sont pas publiés.

## Pourquoi créer un paquet personnalisé ?

La chaîne de préparation Windows devait pouvoir installer des logiciels qui n'étaient pas distribués sous une forme directement utilisable depuis le dépôt Chocolatey retenu. Un paquet personnalisé permet de formaliser les métadonnées, l'installation silencieuse et les codes retour, puis de le rendre disponible dans le cycle de distribution logicielle.

## Architecture d'un paquet

Le modèle de travail comporte un manifeste `.nuspec`, un répertoire `tools`, un script `chocolateyInstall.ps1` et un installeur MSI. Le script retrouve le MSI, lui passe les options d'installation silencieuse et informe Chocolatey des codes de retour attendus. Un `3010` indique classiquement qu'un redémarrage est nécessaire, et ne doit pas être confondu avec une installation entièrement finalisée.

Le [paquet public](../chocolatey/msi-package-example/) est un **exemple fictif** avec un nom et une version inventés. Il n'inclut aucun binaire d'origine. Il vérifie une empreinte SHA-256 fournie par un canal de confiance avant l'exécution du MSI, puis utilise `Install-ChocolateyInstallPackage`.

## Points de vigilance

- Éviter d'inclure des mots de passe ou des paramètres de supervision dans un package.
- Contrôler provenance, intégrité, licence et signature du MSI autorisé.
- Documenter les conditions de redémarrage et les codes Windows Installer.
- Tester installation, mise à niveau et éventuellement désinstallation dans un laboratoire.
- Distinguer l'exemple public de la réalisation historique, dont les détails identifiants restent confidentiels.

La création d'un paquet facilite son intégration dans les scripts de préparation Windows. Elle ne valide pas à elle seule la configuration fonctionnelle de l'application une fois installée.
