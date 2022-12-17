import pytesseract
import cv2
import numpy as np
import pyscreenshot
from string import digits
import pyautogui
import pydirectinput
from threading import Thread
from random import randint
import time
import pdb


# x1, y1, x2, y2 for where towers can be placed
PLAY_AREA = [30, 130, 1440, 920]
WATER = [750, 450, 900, 585]

# Tower positions
TOWER_POS = []

# Prices for all tower upgrades on hard
TOWER_UPGRADES_HARD = [
    # Dart
    [150, 235, 325, 1945, 16200],
    [110, 205, 430, 8640, 48600],
    [95, 215, 675, 2160, 25380],
    
    # Boomerang
    [215, 300, 1405, 3240, 34990],
    [190, 270, 1565, 4535, 37800],
    [110, 325, 1405, 2590, 54000],
    
    # Bomb
    [380, 700, 1295, 3890, 59400],
    [270, 430, 1190, 3455, 27000],
    [215, 325, 865, 3025, 37800],
    
    # Tack
    [160, 325, 650, 3780, 49140],
    [110, 245, 595, 2915, 16200],
    [110, 110, 485, 3455, 21600],
    
    # Ice
    [160, 380, 1620, 2375, 30240],
    [245, 485, 3025, 3240, 21600],
    [190, 245, 2430, 2970, 32400],
    
    # Glue
    [215, 325, 2700, 5400, 23760],
    [110, 1945, 3130, 4160, 16200],
    [130, 430, 3670, 3240, 30240],
    
    # Sniper
    [380, 1620, 3240, 5400, 36720],
    [325, 485, 3455, 7775, 15660],
    [430, 430, 3240, 4590, 15660],
    
    # Sub
    [140, 540, 540, 2700, 34560],
    [485, 325, 1510, 14040, 34560],
    [485, 1080, 1190, 3240, 27000],
    
    # Buccaneer
    [380, 595, 3185, 7775, 27000],
    [595, 540, 970, 5290, 28080],
    [195, 430, 2485, 5940, 24840],
    
    # Ace
    [700, 700, 1080, 3240, 44820],
    [215, 380, 970, 19440, 32400],
    [540, 325, 3025, 25270, 91800],
    
    # Heli
    [865, 540, 1890, 21170, 48600],
    [325, 650, 3780, 11340, 32400],
    [270, 380, 3240, 9180, 37800],
    
    # Mortar
    [540, 540, 970, 8640, 38880],
    [325, 540, 970, 5940, 32400],
    [215, 540, 755, 11880, 43200],
    
    # Dartling
    [325, 970, 4050, 11880, 86400],
    [270, 1025, 5510, 5670, 64800],
    [160, 1295, 3670, 17280, 58320],
    
    # Wizard
    [160, 485, 1405, 10800, 34560],
    [325, 1025, 3240, 6480, 56700],
    [325, 325, 1620, 3025, 28620],
    
    # Super
    [2700, 3240, 21600, 108000, 540000],
    [1080, 1510, 8640, 20520, 97200],
    [3240, 1295, 6050, 64800, 216000],
    
    # Ninja
    [325, 380, 920, 2970, 37800],
    [380, 540, 970, 5615, 23760],
    [270, 430, 2430, 5400, 43200],
    
    # Alchemist
    [270, 380, 1350, 3240, 64800],
    [270, 515, 3240, 4860, 48600],
    [700, 485, 1080, 2970, 43200],
    
    # Druid
    [270, 1080, 1780, 4860, 70200],
    [270, 380, 1025, 5400, 37800],
    [110, 325, 650, 2700, 48600],
    
    # Spike
    [865, 650, 2485, 10260, 162000],
    [650, 865, 2700, 5400, 43200],
    [160, 430, 1510, 3780, 32400],
    
    # Village
    [430, 1620, 865, 2700, 27000],
    [270, 2160, 8100, 21600, 43200],
    [540, 540, 10800, 3240, 5400],
    
    # Engineer
    [540, 430, 620, 2700, 34560],
    [270, 380, 920, 14580, 113400],
    [485, 235, 540, 3780, 58320]
]

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def money_OCR():
    while True:
        # Take a screenshot of the games money value
        pic = pyscreenshot.grab(bbox=(343,14,485,65))
        pic.save('money.png')
        
        # Convert the image to cv2
        image = cv2.imread('money.png')
        
        # Grayscale the image and threshhold it
        gray = get_grayscale(image)
        thresh = thresholding(gray)
        
        # Print the image
        money = pytesseract.image_to_string(thresh)
        money = ''.join(c for c in money if c in digits)
        if not money == '':
            return int(money)
            
def place_tower(tower, water=False):
    pydirectinput.press(tower)
    for i in range(5):
        if not water:
            x1 = randint(PLAY_AREA[0], PLAY_AREA[2])
            y1 = randint(PLAY_AREA[1], PLAY_AREA[3])
        else:
            x1 = randint(WATER[0], WATER[2])
            y1 = randint(WATER[1], WATER[3])
        start_money = money_OCR()
        pydirectinput.click(x1, y1)
        end_money = money_OCR()
        if end_money < start_money:
            TOWER_POS.append([x1,y1])
            return
        
        
            

def main():
    while True:
        money = money_OCR()
        if money > 450:
            tower = randint(1,3)
            if tower == 1: 
                place_tower('e')
            elif tower == 2:
                place_tower('d')
            elif tower == 3:
                place_tower('c', True)
    
    
if __name__ == "__main__":
    time.sleep(3)
    main()