from math import sin, pi, floor

sign = lambda a: (a>0) - (a<0)

class Runnable:
	def __init__(self, func, args=[]):
		self.func = func
		self.args = args
		
	def run(self):
		self.func(*self.args)


def limit(val, lim=1):
	lim = abs(lim)
	return max(-lim, min(val, lim))


def correct_angle(angle):
	return angle + 360 * floor(0.5 - angle / 360)

def deadband(num):
	return 0 if abs(num) < 0.18 else (num - (0.18 * sign(num))) * 1.22

def sinScale(val, non_linearity, passes, lim):
	# 
	# * recursive sin scaling! :D
	# *
	# * :param val: input :param non_linearity: :param passes: how many times
	# * to recurse :return: scaled val
	# 
	scaled = lim * sin(pi / 2 * non_linearity * val) / sin(pi / 2 * non_linearity)
	if passes == 1:
		return scaled
	else:
		return sinScale(scaled, non_linearity, passes - 1, lim)

def wrap_accumulator(acc):
	if acc > 1:
		acc -= 1
	elif acc < -1:
		acc += 1
	else:
		acc = 0
	return acc
		