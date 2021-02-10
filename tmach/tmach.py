import sys

from tmach_def import *

class TMachine(object):
	def __init__(self, inst_size=1024, data_size=1024, num_regs=8):
		self.regs = [0 for _ in range(num_regs)]
		self.IMem = [Instruction() for _ in range(inst_size)]
		self.DMem = [0 for _ in range(data_size)]
		self.DMem = data_size -1

	def get_num(self, token):
		if token.isdigit():
			return (True, int(token))
		else:
			return (False, -1)

	def read_inst(self, f):
		lines = f.readlines()
		for no, line in enumerate(lines):
			line = line.strip()
			if line and line[0] != '*':
				#print(line.split())
				tokens = line.split()
				ret = self.get_num(tokens[0][0:-1])

				if not ret[0]:
					return self.error("Incorrect Memory Location", no+1, -1);
				
				if ret[1] > len(self.IMem):
					return self.error("Location Too Large", no+1, ret[1])			

				if tokens[0][-1:] != ":":
					return self.error("Colon Missing", no+1, ret[1])


	def error(self, msg, lineNo, instNo):
		errmsg = f"Line {lineNo}"
		if instNo >= 0:
			errmsg += f"\t(Instruction {instNo}"
		errmsg += f"\t{msg}"
		print(errmsg)
		return False

	def do_command(self):
		return True

if len(sys.argv) != 2:
	print(f"usage: {argv[0]} <filename>",)
	sys.exit()

with open(sys.argv[1], "r") as f:
	print("TMachine simulation (enter h for help)...");

	tmach = TMachine()

	tmach.read_inst(f)

	while True:
			done = tmach.do_command()
			if done : break

	print("Simulation End.")
	pass



