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

# Previous money, used for making sure the OCR gets the correct value
OLD_MONEY = 650

# Print statements on
VERBOSE = True

# x1, y1, x2, y2 for where towers can be placed
PLAY_AREA = [30, 130, 1440, 920]
WATER = [750, 450, 900, 585]

# Tower positions
TOWER_POS = []

# Can place hero
HERO = True

# Tower type to hotkey conversion
# Length of 22
TOWER_HOTKEY = ['q', 'w', 'e', 'r', 't', 'y', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'a', 's', 'd', 'f', 'g', 'j', 'k', 'l', 'u']

# Tower place price
# Length of 22
TOWER_PLACE_PRICE = [215, 350, 565, 300, 540, 245, 380, 350, 540, 865, 1730, 810, 920, 405, 2700, 540, 595, 430, 1080, 1295, 430, 585]

# Stores the names of the towers, used in Verbose mode
TOWER_NAME = ['Dart', 'Boomerang', 'Bomb', 'Tack', 'Ice', 'Glue', 'Sniper', 'Sub', 'Buccaneer', 'Ace', 'Heli', 'Mortar', 'Dartling', 'Wizard', 'Super', 'Ninja', 'Alchemist', 'Druid', 'Spike', 'Village', 'Engineer', 'Hero']

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
        
def can_place(tower_type):
    if VERBOSE:
        print(f'Trying to see if we can place tower type {TOWER_NAME[tower_type]}')
    if tower_type == 21:
        return money_OCR() >= TOWER_PLACE_PRICE[tower_type] and HERO
    return money_OCR() >= TOWER_PLACE_PRICE[tower_type]
            
def place_tower(tower_type):
    # Press the hotkey for the associated tower
    pydirectinput.press(TOWER_HOTKEY[tower_type])
    
    # Try to place the tower 5 times before giving up
    for i in range(5):
        if VERBOSE:
            print(f'Attempt {i+1} to place tower type {TOWER_NAME[tower_type]}')
        # Randomly choose an area inside the playable area to place the tower
        x1 = randint(PLAY_AREA[0], PLAY_AREA[2])
        y1 = randint(PLAY_AREA[1], PLAY_AREA[3])
        start_money = money_OCR()   # Check how much money you have
        pydirectinput.click(x1, y1) # Try to place the tower
        end_money = money_OCR()     # Check to see if your money went down
        
        # If your money went down you successfully placed the tower
        if end_money < start_money:
            # Save the tower location, initialize its upgrades, and save the tower type
            if VERBOSE:
                print(f'Successfully placed tower type {TOWER_NAME[tower_type]} after {i+1} attempts')
            TOWER_POS.append([x1,y1,[0,0,0], tower_type]) 
            if tower_type == 21:
                global HERO
                HERO = False
            return
    if VERBOSE:
        print('Pressing Escape in place_tower()')
    pydirectinput.press('esc')
        
def upgrade_tower():
    # Initialize the variables needed for this function
    viable_upgrade = False
    tower = 0
    upgrade = 0
    
    # Keep looping until a viable upgrade is found
    for i in range(5):
        tower = -1
        # Loop until you select a tower that isn't the hero
        while True:
            # Randomly selects a tower to upgrade
            tower = randint(0, len(TOWER_POS) - 1)
            if TOWER_POS[tower][3] != 21:
                break
    
        # Randomly chooses a path to upgrade
        upgrade = randint(0,2)
        if VERBOSE:
            print(f"Attempt {i+1} to upgrade tower type {TOWER_NAME[TOWER_POS[tower][3]]} with upgrade path {upgrade}")
        viable_upgrade = can_upgrade(tower, upgrade)
        if viable_upgrade:
            break

    if not viable_upgrade:
        return
    
    # Clicks on the tower
    pydirectinput.click(TOWER_POS[tower][0], TOWER_POS[tower][1])
    
    # Based on the choice of upgrade, clicks the appropriate hotkey
    # Then updates the array of upgrades the tower has
    if upgrade == 0:
        pydirectinput.press(',')
        TOWER_POS[tower][2][0] += 1
    elif upgrade == 1:
        pydirectinput.press('.')
        TOWER_POS[tower][2][1] += 1
    else:
        pydirectinput.press('/')
        TOWER_POS[tower][2][2] += 1
    if VERBOSE:
        print(f'Successfully upgraded tower type {TOWER_NAME[TOWER_POS[tower][3]]} with an upgrade to path {upgrade}')
        print('Pressing Escape in upgrade_tower()')
    time.sleep(0.1)
    pydirectinput.press('esc')
        
def can_upgrade(tower, path):
    # Takes the currently upgraded paths on the tower
    current_paths = TOWER_POS[tower][2]
    only_two_paths = True
    upgrarde_past_two = True

    # Checks if the path has been already been upgraded to tier 5
    if current_paths[path] == 5:
        return False

    # Checks if there is at least one upgrade in two of the paths
    if (current_paths[0] > 0 and current_paths[1] > 0) or (current_paths[0] > 0 and current_paths[2] > 0) or (current_paths[2] > 0 and current_paths[1] > 0):
        only_two_paths =  current_paths[path] > 0
        
    # Checks if any of the paths are upgraded to tier 3 already
    if (current_paths[0] or current_paths[1] or current_paths[2]) > 2:
        upgrarde_past_two =  current_paths[path] > 2
    
    # Gets the amount of money you currently have
    # From the TOWER_UPGRADES you get the array that has the tower upgrades for the specific tower
    # Which is equal to the tower_type * 3 + which path you are trying to upgrade
    # You then check for the current paths at the position of which path you are trying to upgrade
    # This will return a single number that you can then check against the amount of money you
    has_enough_money = money_OCR() >= TOWER_UPGRADES_HARD[TOWER_POS[tower][3] * 3 + path][current_paths[path]]
    
    # Only returns true if the AI is trying to upgrade a viable path and you have enough money
    return only_two_paths and upgrarde_past_two and has_enough_money            

def curr_time():
    return round(time.time() * 1000)

def main():
    while True:
        tower = randint(0, 21)
        if can_place(tower):
            place_tower(tower)
        time.sleep(1)
        if len(TOWER_POS) != 0:
            if VERBOSE:
                print("Upgrade time")
            upgrade_tower()
    
if __name__ == "__main__":
    time.sleep(2)
    main()