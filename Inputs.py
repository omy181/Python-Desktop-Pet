is_dragging = False


def set_dragging(state,on_drag_func = None):
    global is_dragging
    is_dragging = state
    
    if state:
       on_drag_func() 


