import mongoose

WebDavState = False

def __poll__():
    import time
    global WebDavState
    while WebDavState:
        time.sleep(0.4)
        mongoose.poll()

def start():
    import _thread
    import network
    if(network.WLAN(network.STA_IF).isconnected()):
        global WebDavState
        if(False == WebDavState):
            mongoose.init()
            WebDavState = True
            _thread.stack_size(8 * 1024)
            _thread.start_new_thread(__poll__, ())
            _thread.stack_size()
            return True
    return False

def close():
    global WebDavState
    WebDavState = False
