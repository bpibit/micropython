import mongoose
import _thread
import time
import network

WebDavState = False
lock = _thread.allocate_lock()

def __poll__():
    global WebDavState
    while WebDavState:
        if lock.acquire():
            mongoose.poll()
            lock.release()
    mongoose.close()
    _thread.exit()

def start():
    global WebDavState
    if(network.WLAN(network.STA_IF).isconnected() and WebDavState == False and mongoose.start()):
        WebDavState = True
        _thread.stack_size(8 * 1024)
        _thread.start_new_thread(__poll__, ())
        _thread.stack_size()
        return True
    return False

def close():
    global WebDavState
    if (WebDavState == True):
        WebDavState = False

