import tkinter as tk
from DesktopPet import window
from DesktopPet import r_menu

def init():    
    r_menu = tk.Menu(window, tearoff = 0) 
    r_menu.add_command(label ="Cut") 
    r_menu.add_command(label ="Copy") 
    r_menu.add_command(label ="Paste") 

def right_click(event):
    try: 
        r_menu.tk_popup(event.x_root, event.y_root) 
    finally: 
        r_menu.grab_release() 