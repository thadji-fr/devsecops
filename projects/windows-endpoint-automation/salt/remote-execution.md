# Salt : administration Windows distante (exemples anonymisés)

**Le Salt Master et les journaux historiques ne font pas partie des sources fournies.** Les commandes ci-dessous sont des exemples de laboratoire, documentés d'après les interfaces Salt officielles. Aucun identifiant de machine, site ou réseau réel n'apparaît.

## Commandes de lecture depuis un Salt Master

```sh
# Tester la réponse des minions (pas un test ICMP)
salt -L 'lab-win-01,lab-win-02' test.ping

# Informations OS, résultats séparés par minion
salt -L 'lab-win-01,lab-win-02' grains.item os osrelease

# Exécuter une commande CMD distante
salt -L 'lab-win-01,lab-win-02' cmd.run 'whoami'

# Exécuter du PowerShell, résultat texte
salt -L 'lab-win-01,lab-win-02' cmd.run 'Get-Service -Name Spooler | Select-Object Name,Status' shell=powershell

# Récupérer code retour + stdout + stderr
salt -L 'lab-win-01,lab-win-02' cmd.run_all 'Get-Service -Name Spooler | Select-Object Name,Status' shell=powershell

# Cibler des machines déclarant Windows (Grains)
salt -G 'os:Windows' grains.item os osrelease
```

Salt sait **cibler**, **exécuter**, **récupérer les retours** et **appliquer des Salt States** (configuration désirée), pour des tâches plus larges que le patching : diagnostic, services, scripts, paramètres et logiciels.

## Cas possible : faire lancer Chocolatey à un poste distant

```sh
salt 'lab-win-01' cmd.run 'choco list --limit-output'
# Après validation en laboratoire :
salt 'lab-win-01' cmd.run_all 'choco upgrade firefox --yes --no-progress'
```

L'exécution de `choco upgrade` reste une opération **Chocolatey**, même si Salt la déclenche et récupère le résultat. Le code d'exemple ne garantit pas que le paquet ou le logiciel sous-jacent soit effectivement au bon niveau.

## Sécurité et limitations

- Contrôler l'appairage et l'autorisation des clés des minions.
- Limiter les cibles et privilèges d'exécution ; éviter les exemples sur tous les postes de production.
- Ne pas envoyer de secrets directement en argument CLI.
- Vérifier sur un environnement de test les modules Salt compatibles avec les versions Windows, Salt et Chocolatey utilisées.
- Pour un diagnostic, différencier minions hors ligne, exécutions en erreur et succès sans changement.

Documentation de référence : [remote execution](https://docs.saltproject.io/en/master/topics/execution/remote_execution.html), [cmd.run](https://docs.saltproject.io/en/latest/ref/modules/all/salt.modules.cmdmod.html), [targeting](https://docs.saltproject.io/en/latest/topics/tutorials/modules.html).
