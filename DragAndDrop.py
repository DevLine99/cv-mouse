import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def draw_rectangle(img, top_left, bottom_right, color, thickness):
    return cv.rectangle(img, top_left, bottom_right, color, thickness)

def main():
    cap = cv.VideoCapture(0)
    hd = HandDetector()

    # สร้างภาพว่างเพื่อทดสอบการวาดสี่เหลี่ยม
    img_test = np.zeros((100, 100, 3), dtype=np.uint8)  # สร้างภาพว่างสีดำขนาด 300x300

    # กำหนดค่าการวาดสี่เหลี่ยมบนภาพ
    top_left = (100, 100)
    bottom_right = (200, 200)
    color = (0, 255, 0)  # สีเขียวในรูปแบบ BGR
    thickness = 2  # ความหนาของเส้น

    img_test = draw_rectangle(img_test, top_left, bottom_right, color, thickness)

    x, y = 100, 100
    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv.flip(img, 1)
        hands, img = hd.findHands(img, flipType=False)

        if hands:
            lm = hands[0]['lmList']
            length, info, imag = hd.findDistance(lm[8][0:2], lm[4][0:2], img)

            # ถ้าระยะห่างนิ้วชี้ < นิ้วโป้ง
            if length < 20:
                pointer = lm[8]
                if x < pointer[0] < x + img_test.shape[1] and y < pointer[1] < y + img_test.shape[0]:
                    x, y = pointer[0] - img_test.shape[1] // 2, pointer[1] - img_test.shape[0] // 2

        # วาดสี่เหลี่ยมบนภาพที่ได้จากกล้อง
        img_with_rectangle = img.copy()
        img_with_rectangle = draw_rectangle(img_with_rectangle, (x, y), (x + img_test.shape[1], y + img_test.shape[0]), color, thickness)
        
        cv.imshow('frame', img_with_rectangle)

        key = cv.waitKey(1)
        if key != -1:
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
