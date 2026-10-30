# Matrice de validation du portfolio Windows

| Composant | Fondement | Vérification manquante |
| --- | --- | --- |
| Serveur PXE | Contexte fourni oralement, fichiers serveur non transmis | Produit d'amorçage, chaîne réelle de staging |
| Unattended UEFI | Partitionnement et passes présents dans les XML d'origine | Validation Windows SIM et installation VM |
| SetupComplete | Script source identifié | Tests du contexte Windows Setup et droits de lancement |
| RunOnce | Séquencement présent dans les Batch | Connexion admin et enchaînement de stage-02 |
| Profils | Branches conditionnelles constatées | Validation d'un profil fictif sur Windows |
| Chocolatey | Commandes et noms de paquets présents | Versions Chocolatey, résultat, gestion des codes 3010 |
| Pilotes | Extraction et dpinst64 observés | Signature et compatibilité du pilote de test |
| Packaging MSI générique | Exemple fictif documentant le principe d'un package personnalisé | MSI de laboratoire autorisé, SHA-256 et test d'installation |
| Salt Minion | Commande d'installation dans les scripts Windows 11 | Vérification de la connexion au Master, de la clé et de l'état du service |
| Administration Salt Master | Usage décrit par l'auteur, pas de commandes Master d'origine | Ciblage, droits, exécution distante et retours sur minions de laboratoire |
| Sécurité | Audit statique des éléments à publier | Revue de licence et validation d'autorisation de partage |

**Statut :** documentation et code reconstruits, non vérifiés en exécution. Ne pas présenter les exemples comme une installation PXE de bout en bout prête à déployer.
