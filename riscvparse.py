import pyparse.pyparsing as pp

returnStack = []


def pushReturn(str, loc, toks):
    global returnStack
    returnStack.append(toks[0])


reg32 = (
    pp.Combine("x31")
    | pp.Combine("x30")
    | pp.Combine("x29")
    | pp.Combine("x28")
    | pp.Combine("x27")
    | pp.Combine("x26")
    | pp.Combine("x25")
    | pp.Combine("x24")
    | pp.Combine("x23")
    | pp.Combine("x22")
    | pp.Combine("x21")
    | pp.Combine("x20")
    | pp.Combine("x19")
    | pp.Combine("x18")
    | pp.Combine("x17")
    | pp.Combine("x16")
    | pp.Combine("x15")
    | pp.Combine("x14")
    | pp.Combine("x13")
    | pp.Combine("x12")
    | pp.Combine("x11")
    | pp.Combine("x10")
    | pp.Combine("x9")
    | pp.Combine("x8")
    | pp.Combine("x7")
    | pp.Combine("x6")
    | pp.Combine("x5")  # alternate link address
    | pp.Combine("x4")
    | pp.Combine("x3")
    | pp.Combine("x2")  # stack pointer
    | pp.Combine("x1")  # return address for a call
    | pp.Combine("x0")  # hardwired as 0
)
register = reg32

immediate = pp.Combine(pp.Suppress("$") + pp.Literal("0x") + pp.Word(pp.hexnums)) | pp.Combine(
    pp.Suppress("$") + pp.Optional("-") + pp.Word(pp.nums)
)

memory_offset = pp.Combine(pp.Optional("-") + pp.Word(pp.nums))
memory_base = register
memory_index = register
memory_scale = pp.Or(["1", "2", "4", "8"])

label = pp.Combine(pp.Word(pp.alphas, pp.alphanums + "_"))

memory = pp.Group(
    pp.Optional(memory_offset, default="OFFSET")
    + pp.Suppress("(")
    + pp.Optional(memory_base, default="BASE")
    + pp.Optional(pp.Suppress(",") + memory_index + pp.Optional(pp.Suppress(",") + memory_scale))
    + pp.Suppress(")")
)


Operands = register | memory | immediate

UnOpInstList = pp.Word(pp.alphas)

UnOpInstructions = UnOpInstList + Operands + pp.Suppress(",") + Operands

BinOpInstList = pp.Word(pp.alphas)

BinOpInstructions = BinOpInstList + Operands + pp.Suppress(",") + Operands + pp.Suppress(",") + Operands

JumpInstList = pp.Word("j" + pp.alphas)

JumpInstructions = JumpInstList + Operands

BranchInstList = pp.Word("b" + pp.alphas)
BranchInstructions = BranchInstList + Operands + pp.alphas
RISCVInst = pp.Group(BinOpInstructions | UnOpInstructions | BranchInstructions | JumpInstructions)

RISCVLanguage = pp.OneOrMore(RISCVInst)


def RISCVParse(asm):
    global returnStack
    myInstructions = RISCVLanguage.parseString(asm, parseAll=True)
    print(pp.Group(UnOpInstList))
    return myInstructions
