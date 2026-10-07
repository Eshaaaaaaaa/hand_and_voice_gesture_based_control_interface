from tkinter import *
import os

root = Tk()
root.title("AI Smart Interface")
root.geometry("400x300")

Label(root, text="AI Hand & Voice Control interface", font=("Arial", 16)).pack(pady=20)

Button(root, text="Hand Gesture Control", width=25, height=2,
       command=lambda: os.system("python hand_control.py")).pack(pady=10)

Button(root, text="Voice Control", width=25, height=2,
       command=lambda: os.system("python voice_control.py")).pack(pady=10)

root.mainloop()
