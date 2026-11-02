# WireGuard : VPS et serveur Linux on-premises

Étude de cas anonymisée associée à [l'article WireGuard sur thadji.fr](https://thadji.fr/wireguard-connecter-un-serveur-linux-on-premises-a-un-vps-sans-ouvrir-de-ports/).

## Architecture

Je relie un VPS public à des serveurs Linux privés par WireGuard. Le site distant initie le tunnel en UDP vers le VPS. Les routeurs des sites privés n'ont pas besoin de redirection entrante ; en revanche le port UDP WireGuard doit être accessible sur le VPS.

Le VPS constitue le point d'entrée public, avec Nginx pour les flux HTTP(S) et Nginx Stream pour les flux TCP/UDP non HTTP. Le serveur applicatif est joint par son adresse VPN, non son adresse publique.

## Principes de configuration

- Les adresses VPN des exemples sont fictives et distinctes des adresses de production.
- Les clés privées ne sont jamais publiées : chaque machine garde les siennes et n'échange que sa clé publique.
- Les fichiers WireGuard sont protégés et le service est géré par wg-quick.
- AllowedIPs sélectionne les destinations d'un peer et vérifie les sources de paquets reçus, mais ne remplace pas un pare-feu.
- PersistentKeepalive sur le pair distant peut aider à maintenir une traduction NAT fonctionnelle.
- Les accès applicatifs sont limités par des règles de filtrage dédiées, et non uniquement par l'existence du tunnel.

## Vérifications et limites

Un état d'interface ne prouve pas une communication. Un handshake récent ne prouve pas le fonctionnement du routage ou de l'application. Un ping valide au mieux la connectivité ICMP ; un test applicatif doit être contrôlé séparément.

Exemples de commandes de diagnostic en lecture seule :

```bash
sudo wg show
ip addr show wg0
ip route show
sudo journalctl -u wg-quick@wg0 -n 40 --no-pager
```

Un contrôle précédent a constaté des handshakes WireGuard sur le hub, mais la matrice de filtrage entre pairs et les tests applicatifs de bout en bout restent à confirmer. Les journaux bruts, adresses et ports réels sont exclus du dépôt.

## Documentation associée

- [Article de blog](https://thadji.fr/wireguard-connecter-un-serveur-linux-on-premises-a-un-vps-sans-ouvrir-de-ports/)
- [Présentation de l'architecture réseau](README.md)
- [Matrice des validations et tests restant à réaliser](validation.md)
- [Exemples Nginx anonymisés](../../examples/nginx/README.md)
- [WireGuard : Quick Start](https://www.wireguard.com/quickstart/)

Les exemples décrivent des choix techniques ; ils ne sont pas des exports de production.
