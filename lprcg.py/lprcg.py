import cv2
import pytesseract

image = cv2.imread('bienso.jpg')
image = cv2.resize(image, (600, 400))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edges = cv2.Canny(gray, 30, 200)

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

plate = None
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    if w/h > 2 and w/h < 6:
        plate = image[y:y+h, x:x+w]
        break

if plate is not None:
    plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    _, plate_thresh = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(plate_thresh, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    print("Biển số nhận được:", text.strip())
else:
    print("Không tìm được biển số!")
