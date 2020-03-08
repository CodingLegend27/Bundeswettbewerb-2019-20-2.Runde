import numpy as np
from PIL import Image
#import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use("ggplot")

SIZE = 10
HM_EPISODES = 25000
MOVE_PENALTY = 1
# für jedes Mal wenn ein Akku um 1 sinkt
BATTERY_REWARD = 25
# wenn alle Batterien leer sind
ALL_BATTERIES_REWARD = 1000

epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 3000

start_q_table = None # oder dateiname zum Laden einer vorhandenen Datei

# vllt verändern
LEARNING_RATE = 0.1
DISCOUNT = 0.95

ROBOTER_N = 1
AKKU_N = 2

# Festlegung der Farben für den Roboter und den Akku
d = {1: (255, 175, 0),
     2: (0, 255, 0)}


class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def __sub__(self):
        return 





