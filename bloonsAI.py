import numpy as np
import pyscreenshot

def main():
    while True:
        # Take a screenshot of the games money value
        pic = pyscreenshot.grab(bbox=(343,14,485,65))
        pic.save('money.png')
        
if __name__ == "__main__":
    main()