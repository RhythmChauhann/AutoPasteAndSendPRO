import pyautogui
import pyperclip
import time
import threading
import json
import keyboard

from tkinter import *
from tkinter import ttk



SAVE_FILE = "settings.json"

def save_settings(text, times, delay):
    data = {"text": text, "times": times, "delay": delay}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_settings():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"text": "", "times": "1", "delay": "0.2"}


cancel_flag = False 



def send_text(start_from_hotkey=False):
    global cancel_flag
    cancel_flag = False

    user_text = text_input.get("1.0", END).strip()
    repeat_times = repeat_entry.get().strip()
    delay = delay_entry.get().strip()

    if not user_text:
        status_label.config(text="Enter some text!")
        return

    if not repeat_times.isdigit() or int(repeat_times) <= 0:
        status_label.config(text="Repeat must be a positive number!")
        return

    try:
        delay = float(delay)
    except:
        status_label.config(text="Delay must be a number!")
        return

    repeat_times = int(repeat_times)

   
    save_settings(user_text, str(repeat_times), str(delay))

    
    send_button.config(state=DISABLED)
    cancel_button.config(state=NORMAL)
    text_input.config(state=DISABLED)
    repeat_entry.config(state=DISABLED)
    delay_entry.config(state=DISABLED)

    progress_bar["maximum"] = repeat_times
    progress_bar["value"] = 0
    percent_label.config(text="0%")

    if not start_from_hotkey:
        status_label.config(text="Sending in 3 seconds… Click target window!")
        time.sleep(3)
    else:
        status_label.config(text="Hotkey triggered!")

    def run():
        global cancel_flag

        for i in range(repeat_times):
            if cancel_flag:
                status_label.config(text="Cancelled!")
                break

            pyperclip.copy(user_text)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")

            progress_bar["value"] = i + 1
            percent = int((i + 1) / repeat_times * 100)
            percent_label.config(text=f"{percent}%")
            root.update_idletasks()

            time.sleep(delay)

        if not cancel_flag:
            status_label.config(text="Done!")
            

       
        send_button.config(state=NORMAL)
        cancel_button.config(state=DISABLED)
        text_input.config(state=NORMAL)
        repeat_entry.config(state=NORMAL)
        delay_entry.config(state=NORMAL)

    threading.Thread(target=run).start()




def cancel_action():
    global cancel_flag
    cancel_flag = True




def hotkey_listener():
    while True:
        keyboard.wait("f8")
        send_text(start_from_hotkey=True)

threading.Thread(target=hotkey_listener, daemon=True).start()



root = Tk()
root.title("Auto Paste & Send PRO")
root.geometry("450x520")
root.resizable(False, False)


settings = load_settings()

Label(root, text="Enter text to send:", font=("Arial", 12)).pack(pady=5)

text_input = Text(root, height=6, width=52, font=("Arial", 11))
text_input.pack(pady=5)
text_input.insert("1.0", settings["text"])

Label(root, text="How many times to send:", font=("Arial", 12)).pack(pady=5)

repeat_entry = Entry(root, font=("Arial", 12), width=10)
repeat_entry.pack()
repeat_entry.insert(0, settings["times"])

Label(root, text="Delay between messages (sec):", font=("Arial", 12)).pack(pady=5)

delay_entry = Entry(root, font=("Arial", 12), width=10)
delay_entry.pack()
delay_entry.insert(0, settings["delay"])

send_button = Button(root, text="Start", font=("Arial", 13, "bold"), command=send_text)
send_button.pack(pady=15)

cancel_button = Button(root, text="Cancel", font=("Arial", 13), command=cancel_action, state=DISABLED)
cancel_button.pack(pady=5)

progress_bar = ttk.Progressbar(root, length=400)
progress_bar.pack(pady=10)

percent_label = Label(root, text="0%", font=("Arial", 11))
percent_label.pack()

status_label = Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

Label(root, text="Hotkey: Press F8 to instantly send!", font=("Arial", 10, "italic"), fg="blue").pack()

root.mainloop()
