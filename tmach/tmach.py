import sys

from tmach_def import *

class TMachine(object):
	def __init__(self, inst_size=1024, data_size=1024, num_regs=8):
		self.Regs = [0 for _ in range(num_regs)]
		self.IMem = [Instruction() for _ in range(inst_size)]
		self.DMem = [0 for _ in range(data_size)]
		self.DMem = data_size -1

	def get_num(self, token):
		if token.isdigit():
			return (True, int(token))
		else:
			return (False, -1)

	def load_inst(self, token, args, no, loc):
		if token.isalpha():
			
			rr_opcodes = [str(opcode) for opcode in RegRegOpcode]
			rm_opcodes = [str(opcode) for opcode in RegMemOpcode]
			rv_opcodes = [str(opcode) for opcode in RegValOpcode]

			if token in rr_opcodes:   # regreg_opcode
				arg_lst = [int(x) for x in args.split(',')]
				if len(arg_lst) != 3:
					return (error("Argument Error", no, loc), Instruction())

				if arg_lst[0] < 0 or arg_lst[0] >= len(self.Regs):
					return (error("Bad First Register", no, loc), Instruction());

				if arg_lst[1] < 0 or arg_lst[2] >= len(self.Regs):
					return (error("Bad Second Register", no, loc), Instruction());

				if arg_lst[2] < 0 or arg_lst[2] >= len(self.Regs):
					return (error("Bad Thrid Register", no, loc), Instruction());

				return (True, Instruction(token, arg_lst[0], arg_lst[1], arg_lst[2]))
			elif token in rm_opcodes or \
				 token in rv_opcodes: # regval_opcode, regmem_opcode

				arg_lst = args.split(',')
				if len(arg_lst) != 2:
					return (error("Argument Error", no, loc), Instruction())

				if int(arg_lst[0]) < 0 or int(arg_lst[0]) >= len(self.Regs):
					return (self.error("Bad First Register", no, loc), Instruction());

				displacements = arg_lst[1].split('(')
				
				try:
					f_arg = int(displacements[0])
				except ValueError:
					return (self.error("Bad Displacement", no, loc), Instruction())
						
				if len(displacements) != 2:
					return (self.error("Parsing Failed", no, loc), Instruction());

				try:
					s_arg = int(displacements[1][:-1])
					
					if s_arg < 0 or s_arg  >= len(self.Regs):
						return (self.error("Bad Second Register", no, loc), Instruction())	
				except ValueError:
					return (self.error("Bad Second Register(Wrong Register Number Value)", no, loc), Instruction())

				return (True, Instruction(token, arg_lst[0], f_arg, s_arg))
			else:
				return (self.error("Illegal opcode", no, loc), Instruction());
						
		else:
			return (self.error("Missing opcode", no, loc), Instruction());

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
					return self.error("Location Too Large", no + 1, ret[1])			

				if tokens[0][-1:] != ":":
					return self.error("Colon Missing", no + 1, ret[1])

				inst = self.load_inst(tokens[1], tokens[2], no +1, ret[1])
				if inst[0]:
					self.IMem[ret[1]] = inst[1]


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



