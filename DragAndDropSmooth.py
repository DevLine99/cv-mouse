import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def draw_rectangle(img, top_left, bottom_right, color, thickness):
    return cv.rectangle(img, top_left, bottom_right, color, thickness)

def main():
    cap = cv.VideoCapture(0)
    hd = HandDetector()

    # สร้างภาพว่างเพื่อทดสอบการวาดสี่เหลี่ยม
    img_test = np.zeros((100, 100, 3), dtype=np.uint8)  # สร้างภาพว่างสีดำขนาด 100x100

    # กำหนดค่าการวาดสี่เหลี่ยมบนภาพ
    top_left = (100, 100)
    bottom_right = (200, 200)
    color = (0, 255, 0)  # สีเขียวในรูปแบบ BGR
    thickness = 2  # ความหนาของเส้น

    x, y = 100, 100
    x_dest, y_dest = 100, 100
    alpha = 0.1  # ค่าความนุ่มนวล (0.1 = นุ่มนวลมาก, 1 = ไม่มีการนุ่มนวล)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        img = cv.flip(img, 1)
        hands, img = hd.findHands(img, flipType=False)

        if hands:
            lm = hands[0]['lmList']
            length, info, img = hd.findDistance(lm[8][:2], lm[4][:2], img)

            # ถ้าระยะห่างนิ้วชี้ < นิ้วโป้ง
            if length < 20:
                pointer = lm[8]
                x_dest, y_dest = pointer[0] - img_test.shape[1] // 2, pointer[1] - img_test.shape[0] // 2

        # อัพเดตตำแหน่งปัจจุบันเพื่อเพิ่มความนุ่มนวล
        x += (x_dest - x) * alpha
        y += (y_dest - y) * alpha

        # วาดสี่เหลี่ยมบนภาพที่ได้จากกล้อง
        img_with_rectangle = img.copy()
        img_with_rectangle = draw_rectangle(img_with_rectangle, (int(x), int(y)), (int(x + img_test.shape[1]), int(y + img_test.shape[0])), color, thickness)
        
        cv.imshow('frame', img_with_rectangle)

        key = cv.waitKey(1)
        if key != -1:
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
