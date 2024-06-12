import cv2
import numpy as np

# กำหนดขนาดของกล่อง
box_width, box_height = 100, 100
box_x, box_y = 320, 240  # ตำแหน่งเริ่มต้นของกล่อง (ตรงกลางของ画面)

# เปิดกล้อง
cap = cv2.VideoCapture(2)

while True:
    # อ่านเฟรมจากกล้อง
    ret, frame = cap.read()
    
    if not ret:
        print("ไม่สามารถอ่านเฟรมจากกล้องได้")
        break
    
    # วาดกล่องในภาพ
    cv2.rectangle(frame, (box_x, box_y), (box_x + box_width, box_y + box_height), (255, 0, 255), 2)
    
    # แสดงผลภาพ
    cv2.imshow("Frame", frame)
    
    # ตรวจจับการกดคีย์
    key = cv2.waitKey(1)
    
    # หยุดลูปเมื่อกด 'q'
    if key == ord('q'):
        break

    # อ่านพิกัดมือ
    hand_x, hand_y = 0, 0  # สำหรับพิกัดมือ (ให้เริ่มต้นจาก 0, 0)
    
    # ตรวจจับมือ (ในที่นี้เราจะใช้ค่าพิกัดมือจากการกดคีย์เพื่อทดสอบ)
    if key == ord('w'):  # กด 'w' เพื่อย้ายมือขึ้น
        hand_y -= 10
    elif key == ord('a'):  # กด 'a' เพื่อย้ายมือซ้าย
        hand_x -= 10
    elif key == ord('s'):  # กด 's' เพื่อย้ายมือลง
        hand_y += 10
    elif key == ord('d'):  # กด 'd' เพื่อย้ายมือขวา
        hand_x += 10

    # ย้ายกล่องตามมือ
    box_x += hand_x
    box_y += hand_y

# ปล่อยกล้องและปิดหน้าต่าง OpenCV ทั้งหมด
cap.release()
cv2.destroyAllWindows()
