import VRecorder as vr
import tkinter as tk
from tkinter import filedialog
import keyboard as kb

vrobj = vr.VRecorder()
fname = 'user_actions.json'
hk1 =hk2 = hk3 = hk4 = hk5 = None

root = tk.Tk()
root.title("VR Tool v1.0")

app_width = 500
app_height = 180
root.geometry(f"{app_width}x{app_height}")

# Configure grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

button_width = 15
button_bg = "#4CAF50"
button_fg = "white"
button_font = ("Arial", 8, "bold")


def save():
    file_path = filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Script files", "*.json")])
    if file_path:
        global fname
        fname = file_path
        vrobj.recorderSave(file_path)

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Script files", ".json"), ("All files", ".*")])
    if file_path:
        vrobj.playerPlay(file_path)

def exit_app():
    vrobj.playerExit()
    root.destroy()

def activateHK():
    try:
        global hk1, hk2, hk3, hk4, hk5
        hk1 = kb.add_hotkey('ctrl+1', vrobj.recorderStart)
        hk2 = kb.add_hotkey('ctrl+2', vrobj.recorderStop)
        hk3 = kb.add_hotkey('ctrl+3', vrobj.recorderSave)
        hk4 = kb.add_hotkey('ctrl+4', vrobj.playerPlay)
        hk5 = kb.add_hotkey('ctrl+5', vrobj.playerToggle)
        print("Hotkeys are activated")
    except:
        print("eactivated")

def deactivateHK():
    try:
        kb.remove_hotkey(hk1)
        kb.remove_hotkey(hk2)
        kb.remove_hotkey(hk3)
        kb.remove_hotkey(hk4)
        kb.remove_hotkey(hk5)
        print("hotkeys are deactivated")
    except:
        print("deactivated")

record_button = tk.Button(root, text="Record", command=vrobj.recorderStart, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
stop_button = tk.Button(root, text="Stop", command=vrobj.recorderStop, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
save_button = tk.Button(root, text="Save", command=save, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
file_input_button = tk.Button(root, text="Choose and Play", command=choose_file, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
pause_resume_button = tk.Button(root, text="Pause/Resume", command=vrobj.playerToggle, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
exit_button = tk.Button(root, text="Exit", command=exit_app, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
activateHK_button = tk.Button(root, text="Activate Hotkeys", command=activateHK, width=button_width, bg=button_bg, fg=button_fg, font=button_font)
deactivateHK_button = tk.Button(root, text="Deactivate Hotkeys", command=deactivateHK, width=button_width, bg=button_bg, fg=button_fg, font=button_font)

record_button.grid(row=0, column=0, padx=10, pady=10)
stop_button.grid(row=0, column=1, padx=10, pady=10)
save_button.grid(row=0, column=2, padx=10, pady=10)
file_input_button.grid(row=1, column=0, padx=10, pady=10)
pause_resume_button.grid(row=1, column=1, padx=10, pady=10)
exit_button.grid(row=1, column=2, padx=10, pady=10)
activateHK_button.grid(row=2, column=0, padx=10, pady=10)
deactivateHK_button.grid(row=2, column=1, padx=10, pady=10)


kb.add_hotkey('esc', vrobj.playerExit)

# Start the main loop
root.mainloop()