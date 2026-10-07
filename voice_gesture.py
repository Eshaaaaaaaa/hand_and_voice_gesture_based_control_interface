import os
import speech_recognition as sr
import pyautogui
import time
import webbrowser
import keyboard
import psutil
import win32gui

r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.7
r.phrase_threshold = 0.4
r.non_speaking_duration = 0.3
mic = sr.Microphone()

print("🎤 Voice Control Ready")

# ---------- JARVIS TRACKING ----------
start_time = time.time()
app_usage = {}

def get_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

def update_app_usage():
    app = get_active_window()
    if app:
        app_usage[app] = app_usage.get(app, 0) + 1

# ---------- VIRUS CHECK ----------
def check_for_virus():
    suspicious = []
    bad_words = ["miner", "hack", "trojan", "keylog", "rat", "spy", "malware"]

    for proc in psutil.process_iter(['pid', 'name']):
        name = proc.info['name']
        if name:
            lname = name.lower()
            for bad in bad_words:
                if bad in lname:
                    suspicious.append(name)

    if suspicious:
        print("⚠ POSSIBLE THREATS FOUND:")
        for p in suspicious:
            print(" -", p)
        print("👉 Suggestion: Run Windows Defender Full Scan.")
    else:
        print("✅ No suspicious programs detected.")
        print("System looks safe.")

def smooth_scroll(amount):
    x, y = pyautogui.position()
    for _ in range(10):
        pyautogui.moveTo(x, y)
        pyautogui.scroll(amount)
        time.sleep(0.03)

def youtube_scroll(direction):
    amount = -1500 if direction == "down" else 1500
    smooth_scroll(amount)

while True:
    update_app_usage()

    with mic as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.3)
        audio = r.listen(source, phrase_time_limit=4)

    try:
        cmd = r.recognize_google(audio).lower()
        print("You:", cmd)

        # ---------- OPEN ----------
        if "open" in cmd and ("youtube" in cmd or "utube" in cmd):
            webbrowser.open("https://www.youtube.com")
            time.sleep(4)
            pyautogui.moveTo(800, 500)
            pyautogui.click()

        elif "open" in cmd and "whatsapp" in cmd:
            os.system("start whatsapp:")

        elif "open" in cmd and "chrome" in cmd:
            os.system("start chrome")

        elif "open" in cmd and ("file" in cmd or "explorer" in cmd):
            os.startfile("explorer")

        # ---------- CLOSE ----------
        elif "close" in cmd and ("youtube" in cmd or "utube" in cmd):
            pyautogui.hotkey("ctrl", "w")

        elif "close" in cmd and "whatsapp" in cmd:
            os.system("taskkill /f /im WhatsApp.exe")
            os.system("taskkill /f /im WhatsAppBeta.exe")

        elif "close" in cmd and "chrome" in cmd:
            os.system("taskkill /f /im chrome.exe")

        elif "close" in cmd and ("file" in cmd or "explorer" in cmd):
            os.system("taskkill /f /im explorer.exe")

        # ---------- YOUTUBE SCROLL ----------
        elif "scroll" in cmd and "down" in cmd and ("youtube" in cmd or "utube" in cmd):
            youtube_scroll("down")

        elif "scroll" in cmd and "up" in cmd and ("youtube" in cmd or "utube" in cmd):
            youtube_scroll("up")

        # ---------- YOUTUBE PLAY / PAUSE ----------
        elif ("play" in cmd or "pause" in cmd) and ("youtube" in cmd or "utube" in cmd):
            pyautogui.press("space")
            print("YouTube Play / Pause")

        # ---------- GLOBAL SCROLL ----------
        elif "scroll" in cmd and "down" in cmd:
            smooth_scroll(-800)

        elif "scroll" in cmd and "up" in cmd:
            smooth_scroll(800)

        # ---------- ZOOM ----------
        elif "zoom" in cmd:
            if "in" in cmd or "zoomin" in cmd:
                pyautogui.keyDown("ctrl")
                pyautogui.scroll(1200)
                pyautogui.keyUp("ctrl")
                print("Zoom In")

            elif "out" in cmd or "zoomout" in cmd:
                pyautogui.keyDown("ctrl")
                pyautogui.scroll(-1200)
                pyautogui.keyUp("ctrl")
                print("Zoom Out")

        # ---------- JARVIS STATUS ----------
        elif "jarvis" in cmd or "status" in cmd:
            battery = psutil.sensors_battery()
            uptime = int(time.time() - start_time)

            hrs = uptime // 3600
            mins = (uptime % 3600) // 60

            if app_usage:
                most_used = max(app_usage, key=app_usage.get)
            else:
                most_used = "No data yet"

            print("🔋 Battery:", battery.percent, "%")
            print("⏱ Uptime:", hrs, "hrs", mins, "mins")
            print("📱 Most used app:", most_used)

        # ---------- VIRUS CHECK ----------
        elif "virus" in cmd or "security" in cmd:
            check_for_virus()

        elif "exit" in cmd:
            break

        else:
            print("No match")

    except:
        print("Not understood")
