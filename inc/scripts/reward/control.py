import pynput
import time

class Control:
	def __init__(self):
		self.keyboard_controller = pynput.keyboard.Controller()


	def move_character(self, action):
		key_map = {
			None: None,
			0: pynput.keyboard.Key.up,
			1: pynput.keyboard.Key.down,
			2: pynput.keyboard.Key.left,
			3: pynput.keyboard.Key.right,
			4: (pynput.keyboard.Key.up, pynput.keyboard.Key.left),
			5: (pynput.keyboard.Key.up, pynput.keyboard.Key.right),
			6: (pynput.keyboard.Key.down, pynput.keyboard.Key.left),
			7: (pynput.keyboard.Key.down, pynput.keyboard.Key.right),
		}

		if action is None:
			return

		# Use the keyboard controller instance created in the constructor
		keyboard = self.keyboard_controller
		if type(key_map[action]) == tuple:
			keyboard.press(key_map[action][0])
			keyboard.press(key_map[action][1])
			# sleep 1 second
			time.sleep(1)
			keyboard.release(key_map[action][0])
			keyboard.release(key_map[action][1])
		else:
			keyboard.press(key_map[action])
			# sleep 1 second
			time.sleep(1)
			keyboard.release(key_map[action])
