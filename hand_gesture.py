import cv2
import mediapipe as mp
import pyautogui
import math
import time
import webbrowser

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()
last_zoom_time = 0
last_vol_time = 0
last_news_time = 0   # 📰 AI news cooldown

def finger_count(hand):
    fingers = 0
    wrist = hand.landmark[0]

    for tip in [8, 12, 16, 20]:
        if hand.landmark[tip].y < wrist.y:
            fingers += 1

    if hand.landmark[4].x < hand.landmark[3].x:
        fingers += 1

    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

            index = hand.landmark[8]
            thumb = hand.landmark[4]
            wrist = hand.landmark[0]

            # Cursor move
            pyautogui.moveTo(int(index.x * screen_w),
                             int(index.y * screen_h))

            # Pinch = click
            if math.hypot(thumb.x - index.x, thumb.y - index.y) < 0.025:
                pyautogui.click()
                time.sleep(0.35)

            # Fast scroll
            if wrist.y < 0.35:
                pyautogui.scroll(700)
            elif wrist.y > 0.65:
                pyautogui.scroll(-700)

            fingers = finger_count(hand)
            now = time.time()

            # Zoom
            if now - last_zoom_time > 0.12:
                if fingers == 5:
                    pyautogui.hotkey("ctrl", "=")
                    last_zoom_time = now
                elif fingers == 4:
                    pyautogui.hotkey("ctrl", "-")
                    last_zoom_time = now

            # 🔊 VOLUME CONTROL (thumb–index distance)
            dist = math.hypot(thumb.x - index.x, thumb.y - index.y)

            if now - last_vol_time > 0.4:
                if dist > 0.08:
                    pyautogui.press("volumeup")
                    last_vol_time = now

                elif dist < 0.035:
                    pyautogui.press("volumedown")
                    last_vol_time = now

            # 📰 AI NEWS (open palm = 5 fingers)
            if fingers == 6 and now - last_news_time > 5:
                webbrowser.open("ai_news.html")

                last_news_time = now

    cv2.imshow("AI Hand Gesture Interface", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
