import pyautogui
import random
import tkinter as tk
from enum import Enum
import time
from win32api import GetSystemMetrics
from win32gui import GetForegroundWindow, GetWindowText
import sys
from PIL import Image, ImageTk

class State(Enum):
    IDLE = 0   
    SLEEP = 1
    FOLLOW_CURSOR = 2
    DRAGGING = 3
    LOVEING = 4
    WAKEUP = 5
    FALLING = 6
    CELEBRATION = 7
    HUG = 8
    HELP = 9
    WATCHING = 10
    CODER = 11

floor_level = GetSystemMetrics(1)-270

walk_speed = 6
x = 0
y = floor_level
cycle = 0
state_timer = 0
state = State.IDLE
impath = 'Animations/'

is_dragging = False
is_clicked = False
hold_timer = 0

def right_click(event):
    try: 
        r_menu.tk_popup(event.x_root, event.y_root) 
    finally: 
        r_menu.grab_release() 

def on_click(event):
    global is_clicked
    is_clicked = True    

def on_unclick(event):
    global is_clicked,is_dragging,hold_timer
    
    if hold_timer < 2:
        if state == State.SLEEP:
            change_state(State.WAKEUP)
        elif state == State.IDLE:
            change_state(State.LOVEING)
    
    is_clicked = False
    hold_timer = 0
    is_dragging = False

def change_state(new_state):
    global state,state_timer,fall_speed,long_sleep
    
    if new_state != State.SLEEP and long_sleep.get():
        return
    
    state = new_state
    state_timer = 0
    fall_speed = 0
    
def get_res_center_x():
    return GetSystemMetrics(0)/2

def distance(cursor_x,x):
    return abs(cursor_x - x)
 
def move_toward_mouse(cursor_x):  
    global x
    dir = 1    
    
    if(cursor_x < x):
        dir = -1
    elif(cursor_x >= x):
        dir = 1
        
    x += dir * walk_speed
    
    return dir    

def is_on_ground():
    global y,fall_speed
    return y+fall_speed >= floor_level    

def gravity():
    global y,fall_speed
    
    fall_speed += 10
    if not is_on_ground():
        y += fall_speed
    else:
        fall_speed = 0
        y = floor_level 
        
def get_active_window_title():
    window = GetForegroundWindow()
    title = GetWindowText(window)
    return title

def gif_work(cycle,frames):
    if cycle < len(frames) -1:
        cycle+=1
    else:
        cycle = 0
            
    return cycle

def update_frame(animation):  
    global cycle  
    cycle = gif_work(cycle,animation)
    frame = animation[cycle]    
    window.geometry('200x200+'+str(x)+'+'+str(y))
    label.configure(image=frame)

fall_speed = 0
sleep_time = 0

def check_if_watching():
    title = get_active_window_title()  
    if "YouTube" in title or "Netflix" in title:
        return True
    return False

def check_if_coding():
    title = get_active_window_title()  
    if "Visual Studio" in title:
        return True
    return False

def update():
    global state,cycle,x,y,state_timer,gravity_enabled,fall_speed,is_dragging,hold_timer,is_clicked,sleep_time
    
    cursor_x, cursor_y = pyautogui.position()
    if is_clicked:
        hold_timer += 1
        if hold_timer > 1:
            change_state(State.DRAGGING)   
            is_dragging = True  
    else:
        hold_timer = 0
        is_dragging = False
        
        
    if int(time.time()%60)%15 < 1 :
        if check_if_watching() :
           change_state(State.WATCHING)
        elif check_if_coding() :
           change_state(State.CODER)

       
           
    
    match state:
        case State.CODER:
            state_timer += 1
            
            update_frame(coder)      

            time.sleep(0.4) 
            
            if(state_timer > 5):
                if not check_if_coding():
                   change_state(State.IDLE) 
                state_timer = 0
                
        case State.WATCHING:
            state_timer += 1
            
            if x < get_res_center_x():
                update_frame(watching_left)
            else:
                update_frame(watching_right)        

            time.sleep(0.4) 
            
            if(state_timer > 5):
                if not check_if_watching():
                   change_state(State.IDLE) 
                state_timer = 0
            
        case State.HELP:
            lcycle = gif_work(cycle,help)
                        
            if(lcycle == 0):
                change_state(State.IDLE)
            else:
                update_frame(help)   
                time.sleep(0.2)
        
        case State.HUG:
            lcycle = gif_work(cycle,hug)
                        
            if(lcycle == 0):
                change_state(State.IDLE)
            else:
                update_frame(hug)   
                time.sleep(0.2)
            
        case State.CELEBRATION:
            lcycle = gif_work(cycle,celebration)
                        
            if(lcycle == 0):
                change_state(State.IDLE)
            else:
                update_frame(celebration)   
                time.sleep(0.2)    
                
        case State.FALLING:
            gravity()
            time.sleep(0.02)
            update_frame(idle)
            if fall_speed == 0:
                change_state(State.IDLE)
            
        case State.DRAGGING:
            if not is_dragging:
                change_state(State.IDLE)
          
            x = cursor_x-100
            y = cursor_y-50
            time.sleep(0.06)
            update_frame(hold)  
            
        case State.IDLE:
            state_timer += 1      
            
            if(not stay_still.get() and distance(cursor_x,x) > 700):
                change_state(State.FOLLOW_CURSOR)
                
            if gravity_enabled.get() and not is_on_ground():
                change_state(State.FALLING)    
                                                   
            update_frame(idle)
            time.sleep(0.2)
            
            if(state_timer > 100):
                
                random_action =  random.choice([State.SLEEP,State.SLEEP,State.SLEEP,State.WATCHING,State.WATCHING,State.HUG,State.CELEBRATION,State.HELP,State.IDLE,State.IDLE,State.IDLE,State.IDLE])
                   
                sleep_time = random.randint(200,400)
                change_state(random_action)

            
        case State.SLEEP:
            state_timer += 1
            update_frame(sleep)
            time.sleep(0.4) 
            
            if(state_timer > sleep_time):
                change_state(State.WAKEUP)
            
        case State.WAKEUP:    
            lcycle = gif_work(cycle,sleep_to_idle)
                        
            if(lcycle == 0):
                change_state(State.IDLE)
            else:
                update_frame(sleep_to_idle)   
                time.sleep(0.4)    
            
                     
        case State.FOLLOW_CURSOR:
            
            if gravity_enabled.get() and not is_on_ground():
                change_state(State.FALLING)
            
            if(distance(cursor_x,x) < 400):
                change_state(State.IDLE)
            else:    
                dir = move_toward_mouse(cursor_x)  
                time.sleep(0.05)
                if dir == -1:
                    update_frame(walk_positive)
                else:
                    update_frame(walk_negative)                                           
                
        case State.LOVEING:
            
            if gravity_enabled.get() and not is_on_ground():
                change_state(State.FALLING)
                
            time.sleep(0.1)
            update_frame(love)       
            if(cycle == 0):
                change_state(State.IDLE)
            
   
    window.after(5,update)

def start_celebration():
    change_state(State.CELEBRATION)

def set_floor_here():
    global floor_level
    floor_level = y

def set_always_on_top():
    window.wm_attributes('-topmost',always_on_top.get()) 
    
def set_long_sleep():
    if long_sleep.get():
        change_state(State.SLEEP) 
    else:
        change_state(State.WAKEUP)
        
def set_hug():
    change_state(State.HUG)
    
def set_help():
    change_state(State.HELP)
    
def set_love():
    change_state(State.LOVEING)
    
window = tk.Tk()

# Helper function to load images with transparency handled
def load_images(file_path, frames):
    images = []
    for i in range(frames):
        img = Image.open(file_path)
        img.seek(i)
        photo = ImageTk.PhotoImage(img.convert("RGBA"))
        images.append(photo)
    return images

# Load animations with transparency handled
idle = load_images(impath+'Bunidle.gif', 2)
hold = load_images(impath+'BunHold.gif', 4)
sleep = load_images(impath+'BunSleep.gif', 4)
sleep_to_idle = load_images(impath+'BunWake.gif', 4)
walk_positive = load_images(impath+'BunWalkLeft.gif', 5)
walk_negative = load_images(impath+'BunWalkRight.gif', 5)
love = load_images(impath+'BunLove.gif', 9)
celebration = load_images(impath+'BunCelebration.gif', 25)
hug = load_images(impath+'BunHug.gif', 15)
help = load_images(impath+'BunHelp.gif', 16)
watching_left = load_images(impath+'BunWatchLeft.gif', 2)
watching_right = load_images(impath+'BunWatchRight.gif', 2)
coder = load_images(impath+'BunCoder.gif', 2)

#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
window.bind('<ButtonRelease-1>', on_unclick)
window.bind('<Button-1>', on_click)
window.bind("<Button-3>", right_click) 

label.pack()

gravity_enabled = tk.BooleanVar()
always_on_top = tk.BooleanVar(value= True)
long_sleep = tk.BooleanVar()
stay_still = tk.BooleanVar()

set_always_on_top()

r_menu = tk.Menu(window, tearoff = 0) 
r_menu.add_command(label ="Love", command = set_love)
r_menu.add_command(label ="Hug", command = set_hug)
r_menu.add_command(label ="Surprise", command = start_celebration)
r_menu.add_command(label ="Support", command = set_help)
r_menu.add_checkbutton(label ="Winter sleep",onvalue=True,offvalue=False,variable=long_sleep,command=set_long_sleep)
r_menu.add_separator()
r_menu.add_checkbutton(label ="Gravity",onvalue=True,offvalue=False,variable=gravity_enabled)
r_menu.add_checkbutton(label ="Always on top",onvalue=True,offvalue=False,variable=always_on_top,command=set_always_on_top)
r_menu.add_checkbutton(label ="Stay still",onvalue=True,offvalue=False,variable=stay_still)
r_menu.add_command(label ="Set floor here", command = set_floor_here)
r_menu.add_separator()
r_menu.add_command(label ="Bye Bye", command = sys.exit)

#loop the program
window.after(1,update)
window.mainloop()
