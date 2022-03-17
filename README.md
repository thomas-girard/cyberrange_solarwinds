# cyberrrange

![](img/sunburst.png)

Doc intéressante : 
- https://www.mandiant.com/resources/sunburst-additional-technical-details
- https://github.com/CyberSecOps/SolarWinds-Sunburst-Solorigate-Supernova-FireEye



## Compiler en .exe

Pour installer l'outil, lancer la commande : `pip install auto-py-to-exe`. cf : https://pypi.org/project/auto-py-to-exe/

Pour compiler en .exe, lancer `auto-py-to-exe` et indiquer les informations requises dans l'interface graphique. Le résultat apparait dans le dossier `output`

Attention ! Ne pas oublier de mettre le fichier de config dans la version compilée du malware !

## Pour upload un fichier sur Cyberrange :

Rendre exécutable le fichier : `chmod +x <fichier>`

Le placer dans un .tar : `tar -cvf <tar> <fichier>`