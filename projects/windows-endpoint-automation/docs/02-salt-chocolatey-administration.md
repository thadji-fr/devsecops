# 02 — Administrer plusieurs postes Windows avec Salt ; maintenir les logiciels avec Chocolatey

**Retour d'expérience** — Deux fonctions complémentaires, à ne pas confondre : **Chocolatey gère les logiciels et leurs versions**, tandis que **Salt permet l'administration et l'orchestration à distance sur plusieurs postes**.

## 1. Le point de départ : des postes déjà préparés

La chaîne de déploiement Windows présentée dans [l'étude de cas 01](01-pxe-windows.md) utilise PXE et Unattended, puis des scripts Batch/PowerShell pour préparer Chocolatey, configurer un dépôt interne et installer les applications. Dans les scripts Windows 11 fournis, `installpackages_2.cmd` comporte également une **installation de Salt Minion avec Chocolatey**, avec une configuration de rattachement à un Salt Master.

C'est une transition importante : **Chocolatey fournit les paquets sur un poste**, et **Salt Minion ouvre la possibilité d'administrer ultérieurement la machine depuis le Salt Master**. Le fait d'installer le minion ne prouve pas à lui seul que l'association au Master ou l'acceptation de sa clé a abouti.

## 2. Chocolatey : installation, versions et mises à jour des logiciels

Le dépôt Chocolatey interne rassemble les paquets nécessaires aux logiciels Windows. Un script peut demander l'installation d'un ou plusieurs paquets ; lors de la maintenance, Chocolatey peut aussi les mettre à niveau ou les désinstaller.

```bat
REM Exemples de commandes locales, sur poste de laboratoire
choco source list
choco install 7zip.install firefox -y
choco upgrade firefox -y
choco list --limit-output
```

**Ce n'est pas Salt qui effectue intrinsèquement l'installation des applications :** Chocolatey agit localement sur la machine, que la commande soit lancée depuis une console, un script de déploiement ou à distance au travers d'un outil d'orchestration.

La distinction entre version du **paquet** et version du **logiciel réellement exécuté** reste importante, notamment pour vérifier une mise à jour de sécurité.

## 3. Salt : ciblage, exécution distante et retours

Salt fonctionne notamment avec un **Salt Master** qui diffuse des opérations aux **Salt Minions** autorisés. Il est possible de cibler une machine par son ID, plusieurs IDs par une liste ou un ensemble de machines à partir de leurs informations (Grains).

Exemples sur **machines fictives de laboratoire**, exécutés depuis le Master :

```sh
# Le ping Salt vérifie la réponse du minion, pas ICMP.
salt -L 'lab-win-01,lab-win-02' test.ping

# Inventaire OS sur les deux postes
salt -L 'lab-win-01,lab-win-02' grains.item os osrelease

# Commande distante et résultat par machine
salt -L 'lab-win-01,lab-win-02' cmd.run 'whoami'

# PowerShell distant en lecture seule
salt -L 'lab-win-01,lab-win-02' cmd.run 'Get-Service -Name Spooler | Select-Object Name,Status' shell=powershell

# Exemple : filtrer les minions Windows (Grains)
salt -G 'os:Windows' grains.item os osrelease
```

Les IDs sont inventés. Ces exemples illustrent les fonctions de Salt documentées officiellement, **pas des commandes historiques extraites des journaux du Salt Master** (ces journaux ne figurent pas dans les sources fournies).

L'administration à distance couvre aussi les **scripts PowerShell**, le **contrôle des services**, le **diagnostic** et les **états de configuration** (Salt States), selon les modules disponibles et les droits accordés.

## 4. Exemple de script PowerShell exécuté sur plusieurs postes

```sh
# Contrôle à distance et en lecture seule du service Spooler
salt -L 'lab-win-01,lab-win-02' cmd.run_all 'Get-Service -Name Spooler | Select-Object Name,Status' shell=powershell
```

`cmd.run_all` permet de récupérer les sorties et le code retour, utile pour distinguer une commande échouée d'une réponse vide. Voir la [documentation d'exécution distante](../salt/remote-execution.md).

Un Master pouvant exécuter des commandes avec des privilèges élevés sur les minions, le **ciblage**, le **contrôle des accès**, les **logs** et les **tests à petite échelle** sont essentiels.

## 5. Les mises à jour via Salt : un cas d'usage, pas sa définition

Salt peut déclencher une commande Chocolatey à distance :

```sh
# Exemple de laboratoire, non exécuté sur un parc réel ici :
salt 'lab-win-01' cmd.run 'choco upgrade firefox --yes --no-progress'
```

Il peut également appliquer un état déclaratif comme `chocolatey.upgraded`. L'[état de démonstration](../salt/states/browser-update.sls) illustre cette possibilité, mais Salt ne remplace pas le gestionnaire de paquets : il demande au minion d'agir sur le poste.

La correction d'une CVE est **un motif possible** de mise à jour d'application. Elle demande néanmoins de qualifier la version corrigée et de vérifier le résultat. Cela ne résume ni Salt ni Chocolatey.

## 6. Ce que je peux documenter sans sur-vendre

**Établi par les archives :** installation de logiciels avec Chocolatey, dépôt local et scripts Windows 11 ; installation du Salt Minion pendant la préparation du poste.

**Établi par le retour d'expérience déclaré :** utilisation de Salt pour piloter plusieurs machines à distance, dont l'exécution d'actions et de mises à jour.

**Non documenté par les archives :** configuration exacte du Master, règles de ciblage utilisées, nombre de postes, historique réel des commandes, droits précis et résultats chiffrés. Le code publié est donc fictif et doit être validé sur un laboratoire.

## 7. Sources techniques

- [Salt — Remote Execution](https://docs.saltproject.io/en/master/topics/execution/remote_execution.html)
- [Salt — cmd.run, PowerShell et cmd.run_all](https://docs.saltproject.io/en/latest/ref/modules/all/salt.modules.cmdmod.html)
- [Salt — States](https://docs.saltproject.io/en/latest/ref/states/all/)
- [Chocolatey — Install](https://docs.chocolatey.org/en-us/choco/commands/install/)
- [Chocolatey — Upgrade](https://docs.chocolatey.org/docs/commands-upgrade/)
