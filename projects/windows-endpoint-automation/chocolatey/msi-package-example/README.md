# Paquet MSI Chocolatey fictif

Ce dossier illustre la structure technique d'un paquet personnalisé **sans identifier le logiciel historique**. Le nom `portfolio-msi-example` et la version `1.0.0` sont inventés.

Le paquet n'embarque aucun MSI. Pour une exécution dans un laboratoire autorisé, fournir un MSI compatible et son empreinte SHA-256 de confiance dans `PORTFOLIO_MSI_SHA256`. Aucune configuration applicative ni aucun identifiant n'est inclus.

La logique PowerShell vérifie la présence d'un unique MSI, calcule son hash, puis appelle l'installation silencieuse via Chocolatey. Ce code est **non validé en exécution**.
