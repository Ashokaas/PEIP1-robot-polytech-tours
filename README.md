# robot-polytech-tours

Ce document va vous aider (j'espère) à éviter les problèmes qui ne sont pas indiqués dans les polycopiés  qu'on vous a remis.

(mon `main.py` est désastreux mais normalement il remplit les critères de la catégorie 1)

### 1. Device is busy
```
Device is busy or does not respond. Your options:
  - wait until it completes current work;
  - use Ctrl+C to interrupt current work;
  - reset the device and try again;
  - check connection properties;
  - make sure the device has suitable MicroPython / CircuitPython / firmware;
  - make sure the device is not in bootloader mode.
```

Ici le problème vient d'un ou des 2 moteurs. Dans ce cas là, pour executer votre code vous devez :
  - Débrancher les moteurs
  - Executer votre code
  - Rebrancher les moteurs

### 2. PWM Configuration failed

Cette erreur ce produit de temps en temps lorsque vous executez votre code depuis <a href="https://github.com/thonny/thonny">Thonny</a>. Il suffit simplement d'appuyer sur le bouton "Soft reset" de votre carte d'extension (le gros bouton noir). Ce bouton ne réinitialise pas votre robot il va relancer votre code.


### Odométrie qui ne fonctionne pas

Si ça n'a pas changé depuis 2023, les librairies d'odométrie et d'encodeur données ne fonctionnent pas. Redirigez-vous vers les fichiers `ODOMETRIE.py`et `ENCODEUR.py` (c'est pas moi qui les a fait mais on m'a dit wallah ça marche)
