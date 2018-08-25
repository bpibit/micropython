# This file is executed on every boot (including wake-boot from deepsleep)

import utime
import sys
import uos
import _thread

Thread = [ False ]
ReloadFile = ''
ReloadState = False

def GetFileHash():
	global ReloadFile
	return uos.stat(ReloadFile)[8] # Get File Time
	
def __check():
	global ReloadState, Thread
	bak = GetFileHash()
	_thread.start_new_thread(__index, ())
	while(ReloadState):
		utime.sleep(1)
		tmp = GetFileHash()
		if(bak != tmp):
			bak = tmp
			if(Thread[0]):
				Thread[0] = False
				while Thread[0] == False:
					utime.sleep(1)
			_thread.start_new_thread(__index, ())
	_thread.exit()

def __index():
	global ReloadFile, Thread
	Thread[0] = True
	file = open(ReloadFile, "r")
	code = file.read()
	file.close()
	try:
		exec(code, {'Thread' : Thread})
	except Exception as e:
		sys.print_exception(e)
	while Thread[0]:
		utime.sleep(1)
		pass
	Thread[0] = True
	_thread.exit()

def start(file_name):
	global ReloadFile, ReloadState
	ReloadFile = file_name
	ReloadState = True
	ThreadFileCheck = _thread.start_new_thread(__check, ())

def close():
	global ReloadState, Thread
	ReloadState, Thread[0] = False, False
