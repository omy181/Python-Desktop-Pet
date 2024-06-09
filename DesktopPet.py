import pyautogui
import random
import tkinter as tk
from enum import Enum
import time
from win32api import GetSystemMetrics

class State(Enum):
    IDLE = 0   
    SLEEP = 1
    FOLLOW_CURSOR = 2
    DRAGGING = 3
    LOVEING = 4
    WAKEUP = 5
    FALLING = 6
    CELEBRATION = 7


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
            change_state(state.LOVEING)
    
    is_clicked = False
    hold_timer = 0
    is_dragging = False

    
def change_state(new_state):
    global state,state_timer,fall_speed
    state = new_state
    state_timer = 0
    fall_speed = 0

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

floor_level = GetSystemMetrics(1)-270


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

def update():
    
    global state,cycle,x,y,state_timer,gravity_enabled,fall_speed,is_dragging,hold_timer,is_clicked,sleep_time
    
    

    cursor_x, cursor_y = pyautogui.position()
    if is_clicked:
        hold_timer += 1
        if hold_timer > 1:
            change_state(state.DRAGGING)   
            is_dragging = True  
    else:
        hold_timer = 0
        is_dragging = False
    
    match state:
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
            y = cursor_y-20
            time.sleep(0.06)
            update_frame(hold)  
        case State.IDLE:
            state_timer += 1      
            
            if(distance(cursor_x,x) > 1200):
                change_state(State.FOLLOW_CURSOR)
                
            if gravity_enabled.get() and not is_on_ground():
                change_state(State.FALLING)    
                                                   
            update_frame(idle)
            time.sleep(0.2)
            
            if(state_timer > 100):
                sleep_time = random.randint(200,400)
                change_state(State.SLEEP)
            
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
    
window = tk.Tk()

#call buddy's action gif
idle = [tk.PhotoImage(file=impath+'Bunidle.gif',format = 'gif -index %i' %(i)) for i in range(2)]
hold = [tk.PhotoImage(file=impath+'BunHold.gif',format = 'gif -index %i' %(i)) for i in range(4)]
sleep = [tk.PhotoImage(file=impath+'BunSleep.gif',format = 'gif -index %i' %(i)) for i in range(4)]
sleep_to_idle = [tk.PhotoImage(file=impath+'BunWake.gif',format = 'gif -index %i' %(i)) for i in range(4)]
walk_positive = [tk.PhotoImage(file=impath+'BunWalkLeft.gif',format = 'gif -index %i' %(i)) for i in range(5)]
walk_negative = [tk.PhotoImage(file=impath+'BunWalkRight.gif',format = 'gif -index %i' %(i)) for i in range(5)]
love = [tk.PhotoImage(file=impath+'BunLove.gif',format = 'gif -index %i' %(i)) for i in range(9)]
celebration = [tk.PhotoImage(file=impath+'BunCelebration.gif',format = 'gif -index %i' %(i)) for i in range(25)]



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

set_always_on_top()

r_menu = tk.Menu(window, tearoff = 0) 
r_menu.add_checkbutton(label ="Gravity",onvalue=True,offvalue=False,variable=gravity_enabled)
r_menu.add_checkbutton(label ="Always on top",onvalue=True,offvalue=False,variable=always_on_top,command=set_always_on_top)
r_menu.add_command(label ="Set floor here", command = set_floor_here)
r_menu.add_command(label ="Surprise", command = start_celebration)
r_menu.add_separator()
r_menu.add_command(label ="Bye Bye", command = quit)


#loop the program
window.after(1,update)
window.mainloop()