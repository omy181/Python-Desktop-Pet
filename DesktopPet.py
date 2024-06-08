import pyautogui
import random
import tkinter as tk
from enum import Enum
import time
from Inputs import set_dragging, is_dragging
from win32api import GetSystemMetrics

class State(Enum):
    IDLE = 0   
    SLEEP = 1
    FOLLOW_CURSOR = 2
    DRAGGING = 3
    LOVEING = 4
    WAKEUP = 5
    

walk_speed = 6
x = 1400
y = 1000
cycle = 0
state_timer = 0
state = State.IDLE
idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
impath = 'Animations/'

def on_click():
    if state == State.SLEEP:
        change_state(State.WAKEUP)
    elif state == State.IDLE:
        change_state(state.LOVEING)


def change_state_into_drag():
    change_state(state.DRAGGING)

    
def change_state(new_state):
    global state,state_timer
    state = new_state
    state_timer = 0

def distance(cursor_x,x):
    return abs(cursor_x - x)
 
def move_toward_mouse(cursor_x):  
    global x
    global cycle
    
    if(cursor_x < x):
        x-=walk_speed
        frame = walk_positive[cycle]
        
    elif(cursor_x >= x):
        x+=walk_speed
        frame = walk_negative[cycle]
    
    return frame    
      

def gif_work(cycle,frames):
    if cycle < len(frames) -1:
        cycle+=1
    else:
        cycle = 0
            
    return cycle

def update_window(frame):        
    window.geometry('200x200+'+str(x)+'+'+str(y))
    label.configure(image=frame)

acceleration = 0

def update():
    
    global state,cycle,x,y,state_timer,acceleration

    cursor_x, cursor_y = pyautogui.position()
    
    """
    acceleration += 10

    if y >= GetSystemMetrics(1)-300:
        acceleration = 0
        y = GetSystemMetrics(1)-300
        
    y += acceleration
    """
    
    match state:
        case State.DRAGGING:
            if not is_dragging:
                change_state(State.IDLE)
            # drag animation
            x = cursor_x-100
            y = cursor_y-100
            
            cycle = gif_work(cycle,idle)
            frame = idle[cycle]
            update_window(frame)    
        case State.IDLE:
            state_timer += 1
            
            if(distance(cursor_x,x) > 1200):
                change_state(State.FOLLOW_CURSOR)
                           
            cycle = gif_work(cycle,idle)
            frame = idle[cycle]
            time.sleep(0.2)
            update_window(frame)
            
            if(state_timer > 100):
                change_state(State.SLEEP)
            
        case State.SLEEP:
            cycle = gif_work(cycle,sleep)
            frame = sleep[cycle]
            time.sleep(0.2)
            update_window(frame)  
        case State.WAKEUP:           
            cycle = gif_work(cycle,sleep_to_idle)
            if(cycle == 0):
                change_state(State.IDLE)
            else:
                frame = sleep_to_idle[cycle]
                time.sleep(0.2)
                update_window(frame)  
            
                
        case State.FOLLOW_CURSOR:
            if(distance(cursor_x,x) < 400):
                change_state(State.IDLE)
            else:                                           
                cycle = gif_work(cycle,walk_negative)
                frame = move_toward_mouse(cursor_x)
                update_window(frame)
                
        case State.LOVEING:
                       
            cycle = gif_work(cycle,love)
            if(cycle == 0):
                change_state(State.IDLE)
            frame = love[cycle]
            time.sleep(0.1)
            update_window(frame)
            
            

    
    window.after(50,update)

   
    
window = tk.Tk()

#call buddy's action gif
idle = [tk.PhotoImage(file=impath+'Bunidle.gif',format = 'gif -index %i' %(i)) for i in range(2)]
idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif',format = 'gif -index %i' %(i)) for i in range(8)]
sleep = [tk.PhotoImage(file=impath+'BunSleep.gif',format = 'gif -index %i' %(i)) for i in range(4)]
sleep_to_idle = [tk.PhotoImage(file=impath+'BunWake.gif',format = 'gif -index %i' %(i)) for i in range(4)]
walk_positive = [tk.PhotoImage(file=impath+'BunWalkLeft.gif',format = 'gif -index %i' %(i)) for i in range(5)]
walk_negative = [tk.PhotoImage(file=impath+'BunWalkRight.gif',format = 'gif -index %i' %(i)) for i in range(5)]
love = [tk.PhotoImage(file=impath+'BunLove.gif',format = 'gif -index %i' %(i)) for i in range(9)]

#window configuration
window.config(highlightbackground='black')
label = tk.Label(window,bd=0,bg='black')
window.overrideredirect(True)
window.wm_attributes('-transparentcolor','black')
window.wm_attributes('-topmost',1)

window.bind('<Escape>',lambda e: window.quit())
window.bind('<ButtonRelease-1>',lambda e: set_dragging(False))
window.bind('<B1-Motion>', lambda e: set_dragging(True,change_state_into_drag))
window.bind('<Button-1>',lambda e: on_click())

label.pack()

#loop the program
window.after(1,update)
window.mainloop()