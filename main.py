# main.py -- put your code here!
# Fichier main de gestion des ressources du robot

from micropython import const
from machine import Pin
from machine import Timer
from DRV8833 import *
from BME280 import *
from VL6180X import *
import time

from ODOMETRIE import ODOMETRIE


from machine import SD, RTC
import os

#Variables globales pour moteurs et pont en H
DRV8833_Sleep_pin = 'P20' # Pin SLEEP
DRV8833_AIN1 = 'P22' # Entrée PWM moteur A : AIN1
DRV8833_AIN2 = 'P21' # Entrée PWM moteur A : AIN2
DRV8833_BIN1 = 'P19' # Entrée PWM moteur B : BIN1
DRV8833_BIN2 = 'P12' # Entrée PWM moteur B : BIN2


# Vitesse de rotation des roues
V_DEF = (0.73, 1)

    
    
class Robot():
    def __init__(self):
        self.moteur_droit = DRV8833 (DRV8833_AIN1, DRV8833_AIN2, DRV8833_Sleep_pin, 1, 500, 0, 1) # Sur connecteur Encoder1
        self.moteur_gauche = DRV8833 (DRV8833_BIN1, DRV8833_BIN2, DRV8833_Sleep_pin, 1, 500, 2, 3) # Sur connecteur Encoder2

#         self.odometrie = ODOMETRIE(x_pos=0.0, y_pos=0.0, theta=0.0, Delta_T=DELTA_T, Encodeur_Mot_Droit=robot.moteur_droit.encodeur, Encodeur_Mot_Gauche=robot.moteur_gauche.encodeur)

        try:
            rtc = RTC()
            rtc.ntp_sync("pool.ntp.org")
            print(rtc.now())
        except:
            print("impossible de récupérer la date actuelle")


        sd=SD()
        os.mount(sd,'/sd')

        Distance = [-1, -1]
        Luminosite = [-1.0, -1.0]
        
        self.N_VL6180X = const(2)
        VL6180X_CE_Pin = ('P3', 'P7')
        VL6180X_I2C_adr_defaut=const(0x29)
        VL6180X_I2C_Adr=(const(0x2A),const(0x2B),const(0x2C))
        
        print('Config. des broches CE descapteurs VL8160X: debut')
        
        VL6180X_GPIO_CE_Pin=[]
        for pin in VL6180X_CE_Pin:
            VL6180X_GPIO_CE_Pin.append(Pin(pin,mode=Pin.OUT))
            VL6180X_GPIO_CE_Pin[-1].value(0)
            
        bus_i2c=I2C(0,I2C.MASTER,baudrate=400000)
        adr=bus_i2c.scan()
        
        self.capteur_VL6180X=[]
        for i in range (self.N_VL6180X):
            VL6180X_GPIO_CE_Pin[i].value(1) 
            time.sleep(0.002)
            self.capteur_VL6180X.append(VL6180X(VL6180X_I2C_adr_defaut,bus_i2c))
            self.capteur_VL6180X[i].Modif_Adr_I2C(VL6180X_GPIO_CE_Pin[i], VL6180X_I2C_Adr[i],VL6180X_I2C_adr_defaut)
            
            
        
        
        Id_BME280=bus_i2c.readfrom_mem(BME280_I2C_ADR, BME280_CHIP_ID_ADDR,1)
        print ('Valeur Id_BME280 :', hex(Id_BME280[0]))
        
        self.capteur_BME280=BME280(BME280_I2C_ADR, bus_i2c)
        self.capteur_BME280.Calibration_Param_Load()
        
            
    def avancer(self, vitesse:tuple):
        self.moteur_droit.Cmde_moteur(SENS_HORAIRE, vitesse[0])
        self.moteur_gauche.Cmde_moteur(SENS_ANTI_HORAIRE, vitesse[1])
        
        
    def reculer(self, vitesse:tuple) :
        self.moteur_droit.Cmde_moteur(SENS_ANTI_HORAIRE, vitesse[0])
        self.moteur_gauche.Cmde_moteur(SENS_HORAIRE, vitesse[1])
        
        
    def pivoter_droite(self, vitesse:tuple) :
        self.moteur_droit.Cmde_moteur(SENS_ANTI_HORAIRE, vitesse[0])
        self.moteur_gauche.Cmde_moteur(SENS_ANTI_HORAIRE, vitesse[1])
    
    
    def pivoter_gauche(self, vitesse:tuple) :
        self.moteur_droit.Cmde_moteur(SENS_HORAIRE, vitesse[0])
        self.moteur_gauche.Cmde_moteur(SENS_HORAIRE, vitesse[1])
        
        
    def arret(self):
        self.moteur_droit.Arret_moteur()
        self.moteur_gauche.Arret_moteur()
        
        
    def get_distances(self):
        return self.capteur_VL6180X[0].range_mesure(), self.capteur_VL6180X[1].range_mesure()

    
    def get_luminosites(self):
        return self.capteur_d_l_VL6180X[0].ambiant_light_mesure(), self.capteur_d_l_VL6180X[1].ambiant_light_mesure()
        
        
    def get_temp_press_hum(self):
        return {"temp": self.capteur_BME280.read_temp(),
                "press": self.capteur_BME280.read_pression(),
                "hum": self.capteur_BME280.read_humidity()
                }
    
    def enregistrer_donnees(self):
        with open('/sd/donnes.txt', 'a') as f:
            print(str(self.get_temp_press_hum()), file=f)
            
            
    def verif_arret_urgence(self):
        distances = self.get_distances()
        if distances[0] <= 15 or distances[1] <= 15:
            print("Robot : arrêt")
            robot.arret()
            return True
        return False
        
        
    def mode_automatique(self):
        self.continuer_avancer = True
        accu = 0
        while self.continuer_avancer:
            
            self.avancer(V_DEF)
            distances = self.get_distances()
            
            print("Distances : ", distances)
            
            if distances[0] > 50 and distances[1] > 50:
                if accu % 10 == 0:
                    print("Début : enregistrement données")
                    self.enregistrer_donnees()
                    print("Fin : enregistrement données")
                time.sleep(0.1)
                accu += 1
                 
                 
            if self.verif_arret_urgence():
                return
            
            # S'il n'y a au moins un obstacle
            if distances[0] <= 50 or distances[1] <= 50:
                # Si l'obstacle est trop trop proche
                if self.verif_arret_urgence():
                    return
                elif distances[0] < distances[1]:
                    self.arret()
                    print("Robot : tourne à droite")
                    self.pivoter_droite(V_DEF)
                    while distances[0] <= 50 or distances[1] <= 50:
                        if self.verif_arret_urgence():
                            return
                        distances = self.get_distances()
                    robot.arret()
                    
                elif distances[1] < distances[0]:
                    self.arret()
                    print("Robot : tourne à gauche")
                    self.pivoter_gauche(V_DEF)
                    while distances[0] <= 50 or distances[1] <= 50:
                        distances = self.get_distances()
                        if self.verif_arret_urgence():
                            return
                    robot.arret()
            
#             self.odometrie.alarm.callback(None)
#             self.odometrie.alarm.callback(self.odometrie.IT_Delta_x_y_theta)
#             position_x = self.odometrie.x_pos
#             position_y = self.odometrie.y_pos
#             orientation_theta = self.odometrie.theta
        



robot = Robot()
robot.mode_automatique()

