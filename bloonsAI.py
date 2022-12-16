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


# x1, y1, x2, y2 for where towers can be placed
PLAY_AREA = [30, 130, 1440, 920]

# Tower positions
TOWER_POS = []

# Hero Available
HERO = True

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
            
def place_tower(tower):
    pydirectinput.press(tower)
    for i in range(5):
        x1 = randint(PLAY_AREA[0], PLAY_AREA[2])
        y1 = randint(PLAY_AREA[1], PLAY_AREA[3])
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
            tower = randint(1,10)
            if tower <= 5: 
                place_tower('e')
            else:
                place_tower('d')
        print(TOWER_POS)
    
    
if __name__ == "__main__":
    time.sleep(3)
    main()