import servomotor

def aim(x, y):
	x = 1-x

	servomotor.SetAngle((x, y))