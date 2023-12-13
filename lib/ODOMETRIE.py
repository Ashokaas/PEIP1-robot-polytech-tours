from machine import Timer
from micropython import const
from math import pi, cos, sin, fmod
ENCODER_RESOLUTION = const(1400)
WHEEL_RADIUS = 10.0 / 2.0 # cm ; 5.1 cm
WHEEL_DISTANCE = 8.85 #11.4  # distance des points de contacts entre les roues gauche et droite en cm; 8.35 cm
WHEEL_CIRCUMFERENCE = 2.0 * pi * WHEEL_RADIUS # Périmètre de la roue en cm
WHEEL_DTCOEF = WHEEL_CIRCUMFERENCE / ENCODER_RESOLUTION
class Odometry :
    # x : position initiale du robot selon x
    # y : position initiale du robot selon y
    # theta : orientation initiale du robot
    # dt : période d'échantillonnage de l'odométre en ms
    # right_encoder : ressources associés à l'encodeur du moteur droit
    # left_encoder : ressources associés à l'encodeur du moteur gauche

    def __init__ (self, x, y, theta, dt, left_encoder, right_encoder) :
        self.x = x
        self.y = y
        self.theta = theta
        self.dt = dt
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.previous_left_ticks = left_encoder.ticks
        self.previous_right_ticks = right_encoder.ticks
        self.alarm = Timer.Alarm(self.update, ms = dt, periodic = True)
#------------------------------------------------------------------------
    def update(self, arg) :
        delta_left_ticks = self.left_encoder.ticks - self.previous_left_ticks
        delta_right_ticks = self.right_encoder.ticks - self.previous_right_ticks
        self.previous_left_ticks = self.left_encoder.ticks
        self.previous_right_ticks = self.right_encoder.ticks
        delta_left_wheel = WHEEL_DTCOEF * delta_left_ticks * 0.5
        delta_right_wheel = WHEEL_DTCOEF * delta_right_ticks * 0.5
        delta_average = 0.5 * (delta_left_wheel + delta_right_wheel) # distance moyenne parcourue par le robot
        delta_x = delta_average * cos(self.theta)
        delta_y = delta_average * sin(self.theta)
        delta_theta = (delta_right_wheel - delta_left_wheel) / WHEEL_DISTANCE # En radian
        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta
        abs_theta = abs(self.theta)
        if abs_theta > pi:
            self.theta = -self.theta + 2 * fmod(self.theta, pi) # Valeur de theta dans [-Pi, +Pi]
