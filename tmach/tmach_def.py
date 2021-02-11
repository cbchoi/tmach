from enum import Enum, auto

class StrEnum(Enum):
	def _generate_next_value(name, start, count, last_values):
		return name

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name


class RegRegOpcode(StrEnum):
	HALT = auto()
	IN = auto()
	OUT = auto()
	ADD = auto()
	SUB = auto()
	MUL = auto()
	DIV = auto()
	UNK = auto()

class RegMemOpcode(StrEnum):
	LD = auto()
	ST = auto()


class RegValOpcode(StrEnum):
	LDA = auto()
	LDC = auto()
	JLT = auto()
	JLE = auto()
	JGT = auto()
	JGE = auto()
	JEQ = auto()
	JNE = auto()

class Instruction(object):
	def __init__(self, opcode = RegRegOpcode.UNK, arg1=-1, arg2=-1, arg3=-1):
		self.opcode = opcode
		self.arg1 = arg1
		self.arg2 = arg2
		self.arg3 = arg3

class StepResult(StrEnum):
	OKAY = auto()
	HALT = auto()
	IMEM_ERR = auto()
	DMEM_ERR = auto()
	DIV_ZERO = auto()
	INPUT_ERR = auto()