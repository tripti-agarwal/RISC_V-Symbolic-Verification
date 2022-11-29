import pyparse.pyparsing as pp

returnStack = []


def pushReturn(str, loc, toks):
    global returnStack
    returnStack.append(toks[0])


reg32 = (
    pp.Combine("x0")
    | pp.Combine("x1")
    | pp.Combine("x2")
    | pp.Combine("x3")
    | pp.Combine("x4")
    | pp.Combine("x5")
    | pp.Combine("x6")
    | pp.Combine("x7")
    | pp.Combine("x8")
    | pp.Combine("x9")
    | pp.Combine("x10")
    | pp.Combine("x11")
    | pp.Combine("x12")
    | pp.Combine("x13")
    | pp.Combine("x14")
    | pp.Combine("x15")
    | pp.Combine("x16")
    | pp.Combine("x17")
    | pp.Combine("x18")
    | pp.Combine("x19")
    | pp.Combine("x20")
    | pp.Combine("x21")
    | pp.Combine("x22")
    | pp.Combine("x23")
    | pp.Combine("x24")
    | pp.Combine("x25")
    | pp.Combine("x26")
    | pp.Combine("x27")
    | pp.Combine("x28")
    | pp.Combine("x29")
    | pp.Combine("x30")
    | pp.Combine("x31")
)
register = reg32

immediate = pp.Combine(pp.Suppress("$") + pp.Literal("0x") + pp.Word(pp.hexnums)) | pp.Combine(
    pp.Suppress("$") + pp.Optional("-") + pp.Word(pp.nums)
)


Operands = register | immediate

UnOpInstList = pp.Word(pp.alphas)

UnOpInstructions = UnOpInstList + Operands + pp.Suppress(",") + Operands

BinOpInstList = pp.Word(pp.alphas)

BinOpInstructions = BinOpInstList + Operands + pp.Suppress(",") + Operands + pp.Suppress(",") + Operands

RISCVInst = pp.Group(BinOpInstructions | UnOpInstructions)

RISCVLanguage = pp.OneOrMore(RISCVInst)


def RISCVParse(asm):
    global returnStack
    myInstructions = RISCVLanguage.parseString(asm, parseAll=True)
    print(pp.Group(UnOpInstList))
    return myInstructions
