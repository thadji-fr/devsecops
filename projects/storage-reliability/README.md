# Stockage et continuité : ce que j'ai retenu

Une partie des services et données repose sur du **stockage ZFS**. J'ai choisi une organisation avec redondance de disques et un système capable de signaler des erreurs ; cela ne remplace **ni la sauvegarde, ni le test de restauration**.

J'utilise également un **onduleur relié à un serveur**, avec une procédure d'arrêt propre configurée. La présence d'un onduleur ne garantit pas l'autonomie effective sans essai et relevés fiables.

Je distingue trois niveaux :

- **Résilience locale :** alimentation, redondance des disques, état matériel.
- **Sauvegarde :** copies cohérentes, fréquence et protection des accès.
- **Reprise :** capacité à restaurer réellement les données et services.

Je ne publie pas le nombre, le modèle ou l'emplacement exact des disques, ni les chemins de sauvegarde ou les paramètres de déclenchement des arrêts.

→ [Retour d'incident ZFS](zfs-incident.md)
