import mongoose
import _thread
import time
import network

WebDavState = False
lock=_thread.allocate_lock()

def __poll__(delay):
    global WebDavState
    while WebDavState:
        #time.sleep(delay)
        if lock.acquire():
            mongoose.poll()
            lock.release()

 #       try:
 #           time.sleep(delay)
 #           mongoose.poll()
 #       except KeyboardInterrupt:
 #           pass
            
def start():
    if(network.WLAN(network.STA_IF).isconnected()):
        global WebDavState
        if(False == WebDavState):
            mongoose.init()
            WebDavState = True
            _thread.stack_size(8 * 1024)
            _thread.start_new_thread(__poll__, (0.5,))
            _thread.stack_size()
            return True
    return False

def close():
    global WebDavState
    if (WebDavState == True):
        _thread.exit()
        WebDavState = False
