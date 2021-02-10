import sys

from tmach_def import *

class TMachine(object):
	def __init__(self, inst_size=1024, data_size=1024, num_regs=8):
		self.Regs = [0 for _ in range(num_regs)]
		self.IMem = [Instruction() for _ in range(inst_size)]
		self.DMem = [0 for _ in range(data_size)]
		#self.DMem = data_size -1
		self.rr_opcodes = [str(opcode) for opcode in RegRegOpcode]
		self.rm_opcodes = [str(opcode) for opcode in RegMemOpcode]
		self.rv_opcodes = [str(opcode) for opcode in RegValOpcode]

	def get_num(self, token):
		if token.isdigit():
			return (True, int(token))
		else:
			return (False, -1)

	def load_inst(self, token, args, no, loc):
		if token.isalpha():
			if token in self.rr_opcodes:   # regreg_opcode
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
			elif token in self.rm_opcodes or \
				 token in self.rv_opcodes: # regval_opcode, regmem_opcode

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

	def step(self):
		pc = self.Regs[-1]

		if pc < 0 or pc > len(self.IMem):
			return StepResult.IMEM_ERR
		self.Regs[-1] = pc + 1

		# instruction Fetch & Decode
		print(pc, len(self.IMem))
		cur_inst = self.IMem[pc]
		if cur_inst.opcode in self.rr_opcodes:
			r1 = cur_inst.arg1
			r2 = cur_inst.arg2
			r3 = cur_inst.arg3
		elif cur_inst.opcode in self.rm_opcodes:
			r1 = cur_inst.arg1
			r2 = cur_inst.arg3
			m = cur_inst.arg2 + self.Regs[r2]
			if m < 0 or m > len(self.DMem):
				return StepResult.DMEM_ERR
		else:
			r1 = cur_inst.arg1
			r2 = cur_inst.arg3
			m = cur_inst.arg2 + self.Regs[r2]

		# instruction execution
		if cur_inst.opcode == "HALT":
			print("HALT: %1d, %1d, %1d"% (r1,r2,r3))
			return StepResult.HALT
		elif cur_inst.opcode == "IN":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "OUT":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "ADD":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "SUB":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "MUL":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "DIV":
			print(cur_inst.opcode)

		elif cur_inst.opcode == "LD":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "ST":
			print(cur_inst.opcode)

		elif cur_inst.opcode == "LDA":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "LDC":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JLT":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JLE":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JGT":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JGE":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JEQ":
			print(cur_inst.opcode)
		elif cur_inst.opcode == "JNE":
			print(cur_inst.opcode)

		return StepResult.OKAY

	def error(self, msg, lineNo, instNo):
		errmsg = f"Line {lineNo}"
		if instNo >= 0:
			errmsg += f"\t(Instruction {instNo}"
		errmsg += f"\t{msg}"
		print(errmsg)
		return False

	def do_command(self):
		cmd = input("Enter Command:")

		if cmd == "g":
			stepcnt = 0;
			stepResult = StepResult.OKAY
			
			while stepResult == StepResult.OKAY:
				iloc = self.Regs[-1]
				#if ( traceflag ) writeInstruction( iloc ) ;
				stepResult = self.step();
				stepcnt += 1;
				#if  icountflag :
				#	print(f"Number of instructions executed = stepcnt")
			pass

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



