# Traçabilité des reconstructions publiques

Les archives reçues contiennent plusieurs générations de configurations Unattended et de scripts Windows. Leur publication directe n'aurait été ni adaptée ni sûre. Ce tableau établit ce qui reste fidèle aux mécanismes et ce qui a été changé.

| Mécanisme constaté dans les sources | Conservation technique | Transformation volontaire |
|---|---|---|
| XML Unattended UEFI : partitions WinRE 650 Mio, EFI 100 Mio, MSR 16 Mio, Windows étendue | Disposition complète dans le fichier XML public | Suppression des comptes, scripts d'identification et domaines ; Windows SIM non testé |
| Passes windowsPE, offlineServicing, specialize, oobeSystem | Explication de leur rôle et échantillon de plusieurs passes | Paramètres sensibles et jonction au domaine exclus |
| SetupComplete.cmd, puis scripts répartis en deux vagues | SetupComplete, stage-01, stage-02, logs, marqueurs d'état et RunOnce | Connexion automatique et redémarrage forcé retirés |
| Dépôt Chocolatey configuré lors de la préparation | Script de déclaration d'une source Chocolatey | Adresse inventée en .invalid, aucun identifiant |
| Liste standard puis IrfanView/plugins, outils de laboratoire et pilotes | Deux phases, profil applicatif et point d'extension dpinst64 | Aucun pilote ni logiciel propriétaire distribué |
| Ciblage de certaines applications selon l'adresse et le réseau du poste | Sélection conditionnelle d'un profil | Remplacé par DEPLOY_PROFILE ; aucune implantation réseau exposée |
| Agents de supervision / Salt et Wazuh dans l'installation | Documentation de leur fonction dans la chaîne | Pas de configuration de master, d'adresse ni d'identité |
| Paquet Chocolatey personnalisé avec installeur MSI, identité du logiciel non publiée | [Exemple MSI fictif](../chocolatey/msi-package-example/) : manifeste, sélection du binaire, installation silencieuse et codes retour | Produit, version historique, installeur et configuration d'origine exclus |
| Plusieurs pratiques héritées de réduction de protections Windows | Analyse dans l'étude de cas | UAC désactivé, invité SMB et checksums ignorés non reproduits |

## Limites fondamentales

Les fichiers fournis ne prouvent ni le produit exact hébergeant PXE, ni le nombre de postes, ni les temps de déploiement ou de réponse CVE, ni la version de Salt du parc. Ne pas leur attribuer ces caractéristiques.

Le paquet Chocolatey reconstitué et les scripts publics **ne sont pas des copies littérales** et n'ont pas été testés de bout en bout sur Windows. Ce dépôt illustre les mécanismes pratiqués et les points de vigilance, pas une solution certifiée opérationnelle.

## Sécurité des anciennes séquences

Le retour d'expérience doit être capable de parler de dette technique sans la présenter comme bonne pratique. Les archives contiennent des mécanismes anciens de configuration automatique qui posent problème sur des postes actuels : informations d'accès embarquées, contournements de contrôles d'intégrité, modifications UAC ou configuration SMB moins protectrice. On ne les republie pas comme du code d'exploitation.
