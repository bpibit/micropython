import mongoose
import _thread
import time
import network

WebDavState = False
RequestExit = False
lock=_thread.allocate_lock()

def __poll__(delay):
    global WebDavState, RequestExit
    while WebDavState:
        #time.sleep(delay)
        if lock.acquire():
            if(RequestExit == True):
                RequestExit == False
                _thread.exit()
            mongoose.poll()
            lock.release()

 #       try:
 #           time.sleep(delay)
 #           mongoose.poll()
 #       except KeyboardInterrupt:
 #           pass
            
def start():
    global WebDavState, RequestExit
    if(WebDavState == False):
        #if(network.WLAN(network.STA_IF).isconnected()):
        #if(False == WebDavState):
        mongoose.init()
        WebDavState = True
        _thread.stack_size(8 * 1024)
        _thread.start_new_thread(__poll__, (0.5,))
        _thread.stack_size()
    return WebDavState

def close():
    global WebDavState, RequestExit
    if (WebDavState == True):
        WebDavState = False
        RequestExit = True        
        #while (True):
        #    if(RequestExit == False):
        #        break
        #    if(not lock.locked()):
        #        break
        #_thread.exit()


