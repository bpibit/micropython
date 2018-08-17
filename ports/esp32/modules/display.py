
from machine import Pin
from neopixel import NeoPixel

def NeoPixelPower(bool):
	Pin(2, Pin.OUT).value(bool)

class BpiBitNeoPixel(NeoPixel):

	def __init__(self):
		self.Min, self.Max, self.Sum = 0, 5, 25
		NeoPixel.__init__(self, Pin(4), self.Sum)
		
	def LoadXY(self, X, Y, RGB):
		if self.Min <= X and X < self.Max and self.Min <= Y and Y < self.Max:
			self[int(X) + int(Y) * self.Max] = RGB
		else:
			pass
			# print('NeoPixel Load Over Limit')
			
	def LoadP(self, Pos, RGB):
		if self.Min <= Pos and Pos < self.Sum:
			self[Pos] = RGB
		else:
			pass
			# print('NeoPixel Load Over Limit')
	def Show(self):
		self.write()
	