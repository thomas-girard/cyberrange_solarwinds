# Domain Generation Algorithm (DGA)


## Principe

* 4 modes différents de sous-domaines :
    - durant l'initialisation, le malware envoie le nom de domaine de la victime en prefix.
    - dans le mode 'actif', le malware envoie d'autres infos comme la liste des services actifs ou arrêtés ou bien la date

## Encodage de l'hostname :

* si tous les caractères du nom sont dans "0123456789abcdefghijklmnopqrstuvwxyz-_.", alors l'un des algo est utilisé
* Sinon Base64Encode est utilisé et "00" est ajouté à l'encodage => moyen de savoir quelle méthode est utilisée.

* Si le hostname est trop long : il est coupé en 2


* ID est crée :
    * adresse mac du premier réseau disponible
    * nom de domaine
    * HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\MachineGuid value

    * Sunburst prend le MD5 de ces 3 valeurs et l'encode.



## doc intéressante
    - https://blog.cloudflare.com/a-quirk-in-the-sunburst-dga-algorithm/
    - https://github.com/RedDrip7/SunBurst_DGA_Decode
    - https://mp.weixin.qq.com/s/v-ekPFtVNZG1W7vWjcuVug
    - https://symantec-enterprise-blogs.security.com/blogs/threat-intelligence/solarwinds-unique-dga



