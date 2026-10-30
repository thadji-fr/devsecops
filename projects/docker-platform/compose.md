# Docker Compose : volumes, réseaux et publication

J'utilise Compose pour garder des stacks lisibles et reproductibles. Trois notions méritent d'être séparées :

1. **Bind mount** : dossier de l'hôte monté dans un conteneur. Son mode `read-only` ou lecture/écriture se décide selon le besoin réel.
2. **Réseau Docker** : permet aux services du même réseau de communiquer via leur nom et leur port interne.
3. **Publication d'un port** : ouvre un accès depuis l'hôte vers un conteneur, éventuellement lié à une adresse précise de l'hôte.

Dans mon infrastructure, Nginx peut donc atteindre un service **par son nom sur le réseau Docker** même lorsque le port de celui-ci n'est publié que sur `127.0.0.1` côté hôte. Ce choix simplifie les configurations, mais ne crée **pas** de segmentation entre conteneurs d'un même réseau.

Je préfère aussi utiliser des montages de journaux **en lecture seule** lorsqu'un composant doit lire les logs d'un autre sans avoir à les modifier. C'est un principe de réduction des droits, pas une preuve que la sécurité est complète.

## Points de vigilance

- Vérifier qui peut lire/écrire sur les dossiers persistants.
- Séparer autant que possible les réseaux d'administration et les réseaux applicatifs.
- Traiter `/var/run/docker.sock` comme une capacité d'administration forte.
- Vérifier les dépendances avant de retirer un port ou un réseau existant.
- Sauvegarder les données de façon cohérente et tester les restaurations.

→ [Reconstruction anonymisée des stacks Compose](../../examples/compose/README.md) · [Retour d'expérience](migration.md)
