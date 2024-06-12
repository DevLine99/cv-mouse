import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands and Drawing modules
capture_hands = mp.solutions.hands.Hands()
drawing_option = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize webcam
camera = cv2.VideoCapture(0)

# Initialize previous mouse coordinates
prev_mouse_x, prev_mouse_y = 0, 0

# Smoothness factor for mouse movement
smoothening = 7

while True:
    success, image = camera.read()
    if not success:
        break
    
    # Flip and convert image to RGB
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image to detect hands
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    
    # Get image dimensions
    image_height, image_width, _ = image.shape
    
    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                
                # Index finger tip
                if id == 8:
                    mouse_x = screen_width * lm.x
                    mouse_y = screen_height * lm.y

                    # Smooth the mouse movement
                    curr_mouse_x = prev_mouse_x + (mouse_x - prev_mouse_x) / smoothening
                    curr_mouse_y = prev_mouse_y + (mouse_y - prev_mouse_y) / smoothening
                    
                    # Move the mouse
                    pyautogui.moveTo(curr_mouse_x, curr_mouse_y)
                    
                    # Draw circle at the index finger tip
                    cv2.circle(image, (x, y), 15, (0, 255, 255), cv2.FILLED)
                    
                    # Update previous mouse coordinates
                    prev_mouse_x, prev_mouse_y = curr_mouse_x, curr_mouse_y
                
                # Thumb tip
                if id == 4:
                    thumb_x, thumb_y = x, y
                    cv2.circle(image, (x, y), 15, (0, 255, 255), cv2.FILLED)
            

        dist = abs(thumb_y - y)
        print(dist)
        if dist < 20:
            pyautogui.click()

    # Display the image
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()
