import mongoose
import _thread
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


class dynamic():
	def __init__(self):
		self.name, self.state = '', False

	def __file_time(self):
		from uos import stat
		return stat(self.name)[8] # Get File Time

	def __check(self):
		import utime
		from uio import StringIO
		from uos import dupterm, dupterm_notify
		exec_fime = "execfile('" + self.name + "')\r\n"
		dupterm(StringIO(exec_fime))
		dupterm_notify(None)
		bak, last_time = self.__file_time(), utime.ticks_ms()
		while(self.state):
			if (utime.ticks_ms() > last_time + 2000):
				tmp, last_time = self.__file_time(), utime.ticks_ms()
				if(bak != tmp and lock.acquire()):
					bak = tmp
					dupterm(StringIO("\x03\x43"))
					dupterm_notify(None)
					dupterm(StringIO(exec_fime))
					dupterm_notify(None)
					lock.release()
		_thread.exit()

	def start(self, file_name):
		self.name, self.state = file_name, True
		_thread.start_new_thread(self.__check, ())

	def close(self):
		self.state = False
