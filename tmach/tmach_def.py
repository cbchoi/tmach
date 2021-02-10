from enum import Enum, auto

class StrEnum(str, Enum):
	def _generate_next_value(name, start, count, last_values):
		return name

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name


class regreg_opcode(StrEnum):
	HALT = auto()
	IN = auto()
	OUT = auto()
	ADD = auto()
	MUL = auto()
	DIV = auto()


class regmem_opcode(StrEnum):
	LD = auto()
	ST = auto()


class regval_opcode(StrEnum):
	LDA = auto()
	LDC = auto()
	JLT = auto()
	JLE = auto()
	JGT = auto()
	JGE = auto()
	JEQ = auto()
	JNE = auto()

class Instruction(object):
	def __init__(self, opcode = regreg_opcode.HALT, arg1=-1, arg2=-1, arg3=-1):
			self.opecode = opcode
			self.arg1 = arg1
			self.arg2 = arg2
			self.arg3 = arg3
