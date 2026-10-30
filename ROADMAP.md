# Roadmap — apprendre, expérimenter, puis documenter

Je sépare les **composants déjà utilisés**, les **contrôles restant à démontrer** et les **technologies à apprendre**. Un dossier dans `labs/` ne signifie pas qu'une technologie tourne en production.

## Pratiques déjà présentes dans mon infrastructure

- Administration Linux, Docker Compose, Nginx, réseaux privés WireGuard.
- Sécurité avec CrowdSec, Authentik (OIDC / Forward Auth) et contrôle d'accès.
- Administration centralisée des environnements Docker avec Arcane.
- Stockage ZFS, suivi des incidents et principes de continuité.

Les détails d'exploitation restent privés ; voir les [projets](projects/README.md) pour les retours d'expérience publics.

## Qualité d'exploitation à approfondir

- Tests de restauration et sauvegardes cohérentes.
- Contrôles de segmentation, chemins d'accès et exposition IPv4/IPv6.
- Vérification du bon fonctionnement des protections, pas seulement de la présence des services.
- Automatisation des déploiements et validation reproductible des changements.

## Labs et objectifs futurs

| Axe | Statut | Dossier |
|---|---|---|
| Ansible et configuration | **À expérimenter** | [Automation](labs/automation/README.md) |
| Pipelines CI/CD et contrôles qualité | **À expérimenter** | [CI/CD](labs/ci-cd/README.md) |
| Terraform / OpenTofu | **À expérimenter** | [IaC](labs/iac/README.md) |
| Observabilité, métriques et alertes | **À expérimenter** | [Observabilité](labs/observability/README.md) |
| Kubernetes / orchestration | **Projet d'apprentissage** | [Kubernetes](labs/kubernetes/README.md) |

Un cluster Kubernetes **multi-sites** pourrait être étudié plus tard, sous réserve de budget, de tests de connectivité, de quorum et de persistance. **Je ne prétends pas en exploiter un aujourd'hui.**
