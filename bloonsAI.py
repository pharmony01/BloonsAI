import pytesseract
import cv2
import numpy as np
import pyscreenshot
from string import digits

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def main():
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
            print(int(money))
    
    
if __name__ == "__main__":
    main()