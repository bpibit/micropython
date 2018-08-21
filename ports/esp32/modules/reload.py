# This file is executed on every boot (including wake-boot from deepsleep)

import time
import sys
import uos
import _thread

Thread = [ False ]
ReloadFile = 'index.py'
ReloadState = False

def GetFileHash():
	global ReloadFile
	return uos.stat(ReloadFile)[8] # Get File Time
	
def __check():
	bak = GetFileHash()
	_thread.start_new_thread(__index, ())
	while(ReloadState):
		time.sleep(1)
		tmp = GetFileHash()
		if(bak != tmp):
			bak = tmp
			if(Thread[0]):
				Thread[0] = False
				while Thread[0] == False:
					time.sleep(1)
			_thread.start_new_thread(__index, ())

def __index():
	global ReloadFile
	Thread[0] = True
	file = open(ReloadFile, "r")
	code = file.read()
	file.close()
	try:
		exec(code, {'Thread' : Thread})
	except Exception as e:
		sys.print_exception(e)
	while Thread[0]:
		time.sleep(1)
		pass
	Thread[0] = True

def start(file_name):
	global ReloadFile
	global ReloadState
	ReloadFile = file_name
	ReloadState = True
	ThreadFileCheck = _thread.start_new_thread(__check, ())

def close():
	Thread[0] = False
	ReloadState = False

if __name__ == "__main__":
	thread_start()
	
