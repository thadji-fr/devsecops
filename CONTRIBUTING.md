# Contribuer

Les contributions portent sur des **exemples de laboratoire, des explications ou des corrections**. Le dépôt n'est pas un support pour les configurations brutes de mon infrastructure.

- Séparer strictement `projects/` (retours d'expérience) et `labs/` (expérimentations).
- Décrire le résultat réellement observé et les limites, sans présenter une piste future comme déjà déployée.
- Utiliser les domaines `example.org` / `example.invalid` et les IP de documentation RFC 5737 dans les exemples.
- Ne jamais ajouter de secrets, `.env` réels, configurations d'accès, captures non expurgées ni journaux opérationnels.
- Exécuter `python3 scripts/check-public.py` et vérifier les liens et fichiers YAML avant publication.

Voir aussi la [politique de publication](docs/publication-policy.md) et le [modèle de projet](templates/PROJECT.md).
