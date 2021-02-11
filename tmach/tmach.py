import sys

from tmach_def import *

class TMachine(object):
	def __init__(self, inst_size=1024, data_size=1024, num_regs=8):
		self.inst_size = inst_size
		self.data_size = data_size
		self.num_regs = num_regs

		self.init_machine()

		self.rr_opcodes = [str(opcode) for opcode in RegRegOpcode]
		self.rm_opcodes = [str(opcode) for opcode in RegMemOpcode]
		self.rv_opcodes = [str(opcode) for opcode in RegValOpcode]

		self.traceflag = True
		self.registerflag = True

	def init_machine(self):
		self.Regs = [int(0) for _ in range(self.num_regs)]
		self.IMem = [Instruction() for _ in range(self.inst_size)]
		self.DMem = [int(0) for _ in range(self.data_size)]
		self.DMem[0] = self.data_size - 1

		self.stepcnt = 0
		self.inst_loc = 0
		self.data_loc = 0

		self.machine_status = StepResult.OKAY

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

				return (True, Instruction(token, int(arg_lst[0]), f_arg, s_arg))
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

	def print_instruction(self, loc, status_flag = False):
		out = "%5d: "%(loc)
		if loc >= 0 and loc < len(self.IMem):
			out += "%6s%3d,"%(self.IMem[loc].opcode, self.IMem[loc].arg1)
			if self.IMem[loc].opcode in self.rr_opcodes:
				out += "%1d,%1d"%(self.IMem[loc].arg2, self.IMem[loc].arg3)
			else:
				out += "%3d(%1d)"%(self.IMem[loc].arg2, self.IMem[loc].arg3)
			if status_flag:
				out += "\tregs:[" + ",".join([ str(s) for s in self.Regs])+"]"
		print(out)

	def step(self):
		pc = self.Regs[-1]

		if pc < 0 or pc > len(self.IMem):
			return StepResult.IMEM_ERR
		self.Regs[-1] = pc + 1

		# instruction Fetch & Decode
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
			val = input("Enter Integer for IN instruction: ")
			try:
				self.Regs[r1] = int(val)
			except ValueError:
				return StepResult.INPUT_ERR

		elif cur_inst.opcode == "OUT":
			print("OUT instruction prints: %d" % self.Regs[r1])
		elif cur_inst.opcode == "ADD":
			self.Regs[r1] = self.Regs[r2] + self.Regs[r3]
		elif cur_inst.opcode == "SUB":
			self.Regs[r1] = self.Regs[r2] - self.Regs[r3]
		elif cur_inst.opcode == "MUL":
			self.Regs[r1] = self.Regs[r2] * self.Regs[r3]
		elif cur_inst.opcode == "DIV":
			if self.Regs[r3] == 0:
				return StepResult.DIV_ZERO
			self.Regs[r1] = self.Regs[r2] / self.Regs[r3]
		elif cur_inst.opcode == "LD":
			self.Regs[r1] = self.DMem[m]
		elif cur_inst.opcode == "ST":
			self.DMem[m] = self.Regs[r1]
		elif cur_inst.opcode == "LDA":
			self.Regs[r1] = m
		elif cur_inst.opcode == "LDC":
			self.Regs[r1] = cur_inst.arg2
		elif cur_inst.opcode == "JLT":
			if self.Regs[r1] < 0: self.Regs[-1] = m
		elif cur_inst.opcode == "JLE":
			if self.Regs[r1] <= 0: self.Regs[-1] = m
		elif cur_inst.opcode == "JGT":
			if self.Regs[r1] > 0: self.Regs[-1] = m
		elif cur_inst.opcode == "JGE":
			if self.Regs[r1] >= 0: self.Regs[-1] = m
		elif cur_inst.opcode == "JEQ":
			if self.Regs[r1] == 0: self.Regs[-1] = m
		elif cur_inst.opcode == "JNE":
			if self.Regs[r1] != 0: self.Regs[-1] = m

		return StepResult.OKAY

	def error(self, msg, lineNo, instNo):
		errmsg = f"Line {lineNo}"
		if instNo >= 0:
			errmsg += f"\t(Instruction {instNo}"
		errmsg += f"\t{msg}"
		print(errmsg)
		return False

	def toggle_print(self, msg, flag):
		if flag:
			print(f"{msg} on.")
		else:
			print(f"{msg} off.")

	def execute(self):
		self.inst_loc = self.Regs[-1]
		if self.traceflag: 
			self.print_instruction(self.inst_loc, self.registerflag)
		stepResult = self.step()
		self.stepcnt += 1;
		
		return stepResult

	def do_command(self):
		cmd = input("Enter Command:")

		cmd = cmd.split()

		if cmd[0] == 'h':
			printf("Commands are:");
			printf("   (s)tep <n>      "\
				"Execute n (default 1) TM instructions")
			printf("   (g)o            "\
				"Execute TM instructions until HALT")
			printf("   (i)Mem <b <n>>  "\
				"Print n IMem locations starting at b")
			printf("   (d)Mem <b <n>>  "\
				"Print n DMem locations starting at b")
			printf("   (t)race         "\
				"Toggle instruction trace")
			printf("   (r)egister         "\
				"Toggle register contents")
			printf("   (c)lear         "\
				"Reset simulator for new execution of program")
			printf("   (h)elp          "\
				"Cause this list of commands to be printed")
			printf("   (q)uit          "\
				"Terminate the simulation")
		elif cmd[0] == "t":
			self.traceflag = not self.traceflag
			self.toggle_print("Tracing now", self.traceflag)
		elif cmd[0] == "r":
			self.registerflag = not self.registerflag
			self.toggle_print("Show register contents now", self.registerflag)
		elif cmd[0] == "p":
			self.countflag = not self.countflag
			self.toggle_print("Printing instruction count now", self.countflag)
		elif cmd[0] == "g":
			while self.machine_status == StepResult.OKAY:
				self.machine_status = self.execute()
			print(f"Total number of instructions executed = {self.stepcnt}")
			pass
		elif cmd[0] == 'i':
			if self.inst_loc == len(self.IMem):
				self.inst_loc = 0
			item = 1
			if len(cmd) == 2:
				try:
					self.inst_loc = int(cmd[1])
				except ValueError:
					print("Check parameter")
			if len(cmd) == 3:
				try:
					self.inst_loc = int(cmd[1])
					item = int(cmd[2])
				except ValueError:
					print("Check parameters")

			try:
				for i in range(item):
					self.print_instruction(self.inst_loc)
					self.inst_loc += 1
			except:
				print("Index out of range")
		elif cmd[0] == 'd':
			if self.data_loc == len(self.DMem):
				self.data_loc = 0
			item = 1
			if len(cmd) == 2:
				try:
					self.data_loc = int(cmd[1])
					item = 1
				except ValueError:
					print("Check parameter")

			if len(cmd) == 3:
				try:
					self.data_loc = int(cmd[1])
					item = int(cmd[2])
				except ValueError:
					print("Check parameters")

			try:
				for _ in range(item):
					print("%5d: %5d"%(self.data_loc, self.DMem[self.data_loc]))
					self.data_loc += 1
			except:
				print("Index out of range")

		elif cmd[0] == 'c':
			self.init_machine()
		elif cmd[0] == 's':
			if len(cmd) > 2:
				try:
					stepcnt = int(cmd[1])
				except ValueError:
					print("Check step number")
			else:
				stepcnt = 1

				if self.machine_status == StepResult.OKAY:
					for _ in range(stepcnt):
						self.machine_status = self.execute()
						if self.machine_status != StepResult.OKAY:
							break;

		elif cmd[0] == "q":
			return False
		else:
			print("Unknown command.")

		print( self.machine_status )

		return True

if len(sys.argv) != 2:
	print(f"usage: {argv[0]} <filename>",)
	sys.exit()

with open(sys.argv[1], "r") as f:
	print("TMachine simulation (enter h for help)...");

	tmach = TMachine()

	tmach.read_inst(f)

	while True:
		done = not tmach.do_command()
		if done : break

	print("Simulation End.")
	pass
