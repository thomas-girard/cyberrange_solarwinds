## Etapes :

* On récupère le nom de domaine généré par le DGA.
* On regarde le DNS A (permet de relier un nom de domaine ou un sous-domaine à l’adresse IP d’un serveur) correspondant, si l'ip correspondante est dans une liste d'IP : arrêt du malware
* Sinon, on trouve l'enregistrement DNS CNAME (L’enregistrement CNAME indique que le nom de domaine est un alias d’un autre nom de domaine canonique) et on récupère un nouveau nom de domaine qui pointe vers le command & control domain
* avec le serveur C2 : requête get & post.

## Paramètres des requêtes Get et Post vers le C2
* Si le malware veut envoyer des données, il met dans le header "application/octet-stream" à la place de "application/json"
* Dans les requêtes Post :
    * "EventType":"Orion"
    * "EventName":"EventManager"
    * des champs en plus "userld", "sessionld", "steps"
        * "steps" : contient les champs “Timestamp”, “Index”, “EventType”, “EventName”, “DurationMs”, “Succeeded”, and “Message”

* Réponse du Malware : les données sont compressées (Deflate), xoré puis partagé parmi plusieurs "Message" (c'est un json) des "steps".
* Chaque "message" est encodé Base64 séparément
* Pas tous les champs des "steps" contribue au malware : l'entier du Timestamp doit avoir le bit "0x2" pour indiquer que le contenu de Message est utilisé par le malware
* les autres champs contiennes des données randoms

* The DNS response will return a CNAME record that points to a Command and Control (C2) domain.
* The C2 traffic to the malicious domains is designed to mimic normal SolarWinds API communications


## Steganographie : de C2 => Malware

* Les réponses http vise à ressembler à celles du framework .NET
* les commandes vers le malware sont cachées dans des strings qui ressemble à des strings GUIDS (globally unique identifier) ou des strings HEX
* les commandes sont extraites du corps de la requête HTTP en cherchant les strings HEX avec l'expression régulière "\{[0-9a-f-]{36}\}"|"[0-9a-f]{32}"|"[0-9a-f]{16}"
* tous les sous-strings récupérés sont mis bout à bout, on enlève les caractères non Hexa et décodé de l'hexa.
* la première valeur DWORD (32-bit unit of data. INTEGER value in the range 0 through 4,294,967,295) est la taille du message suivie immédiatement du message avec ensuite éventuellement des bytes randoms
* Le message extrait est single-byte XOR en utilisant le premier byte du message et ensuite il est décompressé (Deflate)

* La liste des commandes du malware est définie dans le lien ci-dessous

## Documentation
* https://www.mandiant.com/resources/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor

## Ce qui est en place

* le malware récupère le bon nom de domaine du server C2 de l'attaquant
* Il fait des requêtes POST toutes les 10 secondes
* Le malware récupère les ordres de l'attaquant cachées avec de la stegano et les exécutent
* Le malware envoie ces infos de manière cachée à l'attaquant
* Les commandes du hackers sont prévus dans un fichier csv

