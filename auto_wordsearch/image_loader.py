'''
Loads an image into memory
'''
import cv2
from pathlib import Path

root = Path.cwd()
TESTDIR = root/"auto_wordsearch"/"test"
FILENAME = "test1.png"
TESTPATH = TESTDIR/FILENAME
print(TESTPATH)
img = cv2.imread(str(TESTPATH),0)
if img is None:
    print("Image read error")
    exit()
print("Success!")
cv2.imshow('test image', img)
cv2.waitKey(0)