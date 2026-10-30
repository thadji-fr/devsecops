# Salt : administration et orchestration distante

Les scripts de préparation Windows 11 comprennent l'installation de **Salt Minion via Chocolatey**. Une fois rattaché et autorisé auprès d'un Salt Master, ce minion permet l'administration distante du poste.

Salt peut :
- cibler un ou plusieurs minions par nom, liste ou Grains ;
- exécuter des commandes CMD et PowerShell, ainsi que des scripts ;
- consulter des informations système, contrôler des services et récupérer des retours ;
- appliquer des états de configuration ;
- déclencher, si nécessaire, des opérations Chocolatey à distance.

**Salt n'est pas un gestionnaire de paquets** et ne se limite pas à la remédiation des CVE. **Chocolatey reste l'outil Windows chargé de l'installation et de la mise à jour des logiciels.**

Voir les [exemples d'exécution distante](remote-execution.md), la [documentation du cas d'usage](../docs/02-salt-chocolatey-administration.md) et l'[état facultatif de mise à jour](states/browser-update.sls).

Les configurations du Salt Master historique ne figurent pas dans les archives fournies ; les commandes publiques utilisent donc des minions fictifs et ne constituent pas des preuves d'exécution sur le parc original.
