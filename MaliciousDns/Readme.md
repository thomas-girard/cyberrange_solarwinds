## Etapes :

* On récupère le nom de domaine généré par le DGA.
* On regarde le DNS A correspondant, si l'ip correspondante est dans une liste d'IP : arrêt du malware
* Sinon, on trouve l'enregistrement DNS CNAME et on récupère un nouveau nom de domaine qui pointe vers le command & control domain
* avec le serveur C2 : requête get & post. Si le malware veut envoyer des données, il met dans le header "application/octet-stream" à la place de "application/json"



## Documentation
* https://www.mandiant.com/resources/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor
* The DNS response will return a CNAME record that points to a Command and Control (C2) domain.
* The C2 traffic to the malicious domains is designed to mimic normal SolarWinds API communications

