## Etapes :

* Récupération du nom de domaine généré par le DGA.
* Récupération du DNS A (permet de relier un nom de domaine ou un sous-domaine à l’adresse IP d’un serveur) correspondant, si l'IP associée est dans une liste d'IP : arrêt du programme.
* Sinon, recherche de l'enregistrement DNS CNAME (L’enregistrement CNAME indique que le nom de domaine est un alias d’un autre nom de domaine canonique) et on récupère un nouveau nom de domaine qui pointe vers le command & control domain
* Communication avec le serveur C2 : requêtes get & post.

## Steganographie : de C2 => program

* Les réponses http vise à ressembler à celles du framework .NET
* Les commandes vers le program sont cachées dans des strings qui ressemble à des strings GUIDS (globally unique identifier) ou des strings HEX
* Les commandes sont extraites du corps de la requête HTTP en cherchant les strings HEX avec l'expression régulière "\{[0-9a-f-]{36}\}"|"[0-9a-f]{32}"|"[0-9a-f]{16}"
* Tous les sous-strings récupérés sont mis bout à bout, on enlève les caractères non Hexa et décodé de l'hexa.
* Le message extrait est single-byte XOR en utilisant le premier byte du message et ensuite il est décompressé (Deflate)

## Documentation
* https://www.mandiant.com/resources/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor

