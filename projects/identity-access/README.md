# Authentik, OIDC et Forward Auth sur un outil d'administration

Pour centraliser les accès aux outils sensibles, j'utilise **Authentik**. Dans le cas d'un gestionnaire Docker, je l'ai intégré avec **OIDC** et une couche de **Forward Auth côté SWAG/Nginx**.

**Point de vocabulaire : les permissions et le contrôle Forward Auth sont configurés dans Authentik.** SWAG interroge le mécanisme d'autorisation avant de laisser passer la requête ; il ne constitue pas à lui seul la source des règles d'accès.

Dans ma configuration, l'accès est réservé à un compte administrateur autorisé. Les noms de fournisseurs, les règles exactes, les URL d'administration, les identifiants et les paramètres de session ne sont **pas publiés**.

## Les validations importantes

- Le visiteur non authentifié est redirigé/refusé comme prévu.
- Un compte connecté mais **non autorisé** ne peut pas accéder à l'outil.
- Les chemins directs vers le backend ne contournent pas les contrôles du proxy.
- Les cookies, sessions et en-têtes de confiance sont correctement protégés.

L'existence d'un écran de connexion ne suffit pas à prouver l'absence de contournement. Je distingue la **configuration déclarée** de sa **validation de bout en bout**.

→ [Gestion centralisée avec Arcane](../docker-management/README.md) · [Exemple SWAG Forward Auth](../../examples/nginx/arcane-authentik.subdomain.conf)
