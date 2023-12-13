# Fichier de configuration des ressources matérielles
# Bibliothéque ConfigMateriel.py
# Validé le 12.03.2021

# Définition de la broche de la led précablée sur la carte Wipy 3.0
Led_P9_pin = 'P9'

# Ressources de la carte Wipy 3.0 associées au driver DRV8833 des moteurs
#   Pont H_A <=> moteur gauche <=> moteur 1 carte PCB
#   Pont H_B <=> moteur droit <=> moteur 2 carte PCB
DRV8833_Sleep_pin = 'P20'
DRV8833_AIN1_pin = 'P22' # Broche de commande 1 du moteur gauche
DRV8833_AIN2_pin = 'P21' # Broche de commande 2 du moteur gauche
DRV8833_BIN1_pin = 'P12' # Broche de commande 1 du moteur droit
DRV8833_BIN2_pin = 'P19' # Broche de commande 2 du moteur droit

# Ressources de la carte Wipy 3.0 associées aux encodeurs des moteurs
Moteur_Droit_EncodeurA_pin = 'P11' # Broche de la voie A de l'encodeur du moteur droit
Moteur_Droit_EncodeurB_pin = 'P18' # Broche de la voie B de l'encodeur du moteur droit
Moteur_Gauche_EncodeurA_pin = 'P15' # Broche de la voie A de l'encodeur du moteur gauche
Moteur_Gauche_EncodeurB_pin = 'P13' # Broche de la voie B de l'encodeur du moteur gauche

# Id moteurs
Id_Moteur_Droit = 1
Id_Moteur_Gauche = 2

# Ressources de la carte Wipy 3.0 associées aux capteurs de distance - luminosité VL6180X
# # Ressources GPIo de la carte WiPy3.0 affectées au contrôle des capteurs VL6180X
# Quadruplet de broches de la carte Wipy 3.0 (CE_Capteur connecteur1, CE_Capteur connecteur2, CE_Capteur connecteur3, CE_Capteur connecteur4)
VL6180X_CE_Pin = ('P3', 'P5', 'P6', 'P7')
