import cv2 as cv
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import win32com.client

def list_cameras():
    # ใช้ WMI เพื่อดึงข้อมูลกล้องที่เชื่อมต่ออยู่
    wmi = win32com.client.GetObject("winmgmts:")
    cameras = []
    for cam in wmi.InstancesOf("Win32_PnPEntity"):
        if cam.Name and "cam" in cam.Name.lower():
            cameras.append(cam.Name)
    return cameras

def draw_grid(img, rows, cols):
    # คำนวณขนาดของแต่ละเซลล์ในตาราง
    cell_width = img.shape[1] // cols
    cell_height = img.shape[0] // rows
    
    # วาดเส้นแนวนอนเพื่อสร้างตาราง
    for i in range(1, rows):
        y = i * cell_height
        cv.line(img, (0, y), (img.shape[1], y), (0, 255, 0), 1)
    
    # วาดเส้นแนวตั้งเพื่อสร้างตาราง
    for j in range(1, cols):
        x = j * cell_width
        cv.line(img, (x, 0), (x, img.shape[0]), (0, 255, 0), 1)

# แสดงรายการกล้องที่เชื่อมต่ออยู่
cameras = list_cameras()

if not cameras:
    print("ไม่พบกล้องที่เชื่อมต่ออยู่")
    exit()

print("รายการกล้องที่เชื่อมต่ออยู่:")
for i, cam in enumerate(cameras):
    print(f"{i}: {cam}")

# รับหมายเลขกล้องจากผู้ใช้
camera_index = int(input("กรุณาเลือกหมายเลขกล้อง: "))

# สร้างตัวตรวจจับมือ
detector = HandDetector(detectionCon=0.8, maxHands=2)

# เปิดกล้องตามหมายเลขที่ระบุ
cap = cv.VideoCapture(camera_index)

if not cap.isOpened():
    print(f"ไม่สามารถเปิดกล้องหมายเลข {camera_index} ได้")
    exit()

while True:
    # อ่านเฟรมจากกล้อง
    success, img = cap.read()
    
    if not success:
        print("ไม่สามารถอ่านเฟรมจากกล้องได้")
        break
    
    # วาดตารางขนาด 5x5 บนภาพ
    draw_grid(img, 5, 5)
    
    # ตรวจจับมือ
    hands, img = detector.findHands(img)
    # hands, img = detector.findHands(img, draw=False)

    if hands:
        for hand in hands:
             # วาดวงกลมบนจุดที่ตรวจจับได้บนมือและแสดงตำแหน่ง x และ y ของปลายนิ้วชี้
            for id, lm in enumerate(hand["lmList"]):
                # ใช้ตำแหน่งของปลายนิ้วชี้ (index finger) ที่มี index เป็น 8
                if id == 8:
                    # แสดงตำแหน่ง x และ y ของปลายนิ้วชี้
                    x, y = lm[1], lm[2]
                    cv.putText(img, f'(x={x}, y={y}', (0, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    else:
        # ถ้าไม่พบมือ กำหนดค่า x และ y เป็น 0
        x, y = 0, 0
        cv.putText(img, f'x={x}, y={y}', (0, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # แสดงผลภาพ
    cv.imshow("Image", img)
    
    # หยุดลูปเมื่อกด 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# ปล่อยกล้องและปิดหน้าต่าง OpenCV ทั้งหมด
cap.release()
cv.destroyAllWindows()
