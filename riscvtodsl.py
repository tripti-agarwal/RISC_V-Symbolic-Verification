import sys


from RISCVtodslHelper import *
import config
import dslparse


def SetupOperandForShifts32BitRegister(x):
    oldDest = "oldDest"
    tempString = ""

    if Is32Register(x[1]) and (Is32Register(x[2]) and Is32Register(x[3])):
        dest = x[1]
        source1 = x[2]
        source2 = x[3]
        addr = ""
        print("yes")
        return dest, source1, source2, oldDest, addr, tempString
    else:
        sys.exit("SetupOperand32BitUnary operand error: %s" % (x))


def SetupOperandForShifts32BitImmediate(x):
    oldDest = "oldDest"
    tempString = ""

    if Is32Register(x[1]) and (Is32Register(x[2]) and isImmediate(x[3])):
        dest = x[1]
        source1 = x[2]
        source2 = x[3]
        addr = ""
    if Is32Register(x[1]) and (isImmediate(x[2]) and isImmediate(x[3])):
        dest = x[1]
        source1 = x[2]
        source2 = x[3]
        addr = ""
    if Is32Register(x[1]) and (isImmediate(x[2]) and Is32Register(x[3])):
        dest = x[1]
        source1 = x[2]
        source2 = x[3]
        addr = ""

    return dest, source1, source2, oldDest, addr, tempString


def SaveToOperandForShifts32BitRegister(x, dest, source1, source2, oldDest, addr):
    if Is32Register(x[1]) and (Is32Register(x[2]) and Is32Register(x[3])):
        return ""


def SaveToOperandForShifts32BitImmediate(x, dest, source1, source2, oldDest, addr):
    if Is32Register(x[1]) and (Is32Register(x[2]) and isImmediate(x[3])):
        return ""
    if Is32Register(x[1]) and (isImmediate(x[2]) and isImmediate(x[3])):
        return ""
    if Is32Register(x[1]) and (isImmediate(x[2]) and Is32Register(x[3])):
        return ""


def SetupOperand32BitRegister(x):
    oldDest = "oldDest"
    tempString = ""
    if len(x) == 4:
        if Is32Register(x[1]) and (Is32Register(x[2]) or Is32Register(x[3])):
            dest = x[1]
            source1 = x[2]
            source2 = x[3]
            addr = ""

        return dest, source1, source2, oldDest, addr, tempString

    if len(x) == 3:
        if Is32Register(x[1]) and Is32Register(x[2]):
            dest = x[1]
            source = x[2]
            addr = ""

        return dest, source, oldDest, addr, tempString


def SetupOperand32BitImmediate(x):
    oldDest = "oldDest"
    tempString = ""
    if len(x) == 4:
        if Is32Register(x[1]) and (Is32Register(x[2]) or isImmediate(x[3])):
            dest = x[1]
            source1 = x[2]
            source2 = x[3]
            addr = ""
        if Is32Register(x[1]) and (isImmediate(x[2]) or isImmediate(x[3])):
            dest = x[1]
            source1 = x[2]
            source2 = x[3]
            addr = ""
        if Is32Register(x[1]) and (isImmediate(x[2]) or Is32Register(x[3])):
            dest = x[1]
            source1 = x[2]
            source2 = x[3]
            addr = ""

        return dest, source1, source2, oldDest, addr, tempString

    if len(x) == 3:
        if Is32Register(x[1]) and isImmediate(x[2]):
            dest = x[1]
            source = x[2]
            addr = ""

        return dest, source, oldDest, addr, tempString


# right now there is only register binary operations
# will also implement register and immediate binary operations
def SaveToOperand32BitUnary(x, dest, source, oldDest, addr):
    oldDest = "oldDest"
    tempString = ""

    if (Is32Register(x[2]) or isImmediate(x[2])) and Is32Register(x[1]):
        return ""
    else:
        sys.exit("SetupOperand32BitUnary operand error: %s" % (x))


def SaveToOperand32BitRegister(x, dest, source1, source2, oldDest, addr):
    oldDest = "oldDest"
    tempString = ""

    if Is32Register(x[1]) and (Is32Register(x[2]) and Is32Register(x[3])):
        return ""
    else:
        sys.exit("SetupOperand32Bit operand error: %s" % (x))


def SaveToOperand32BitImmediate(x, dest, source1, source2, oldDest, addr):
    oldDest = "oldDest"
    tempString = ""

    if Is32Register(x[1]) and (Is32Register(x[2]) and isImmediate(x[3])):
        return ""
    else:
        sys.exit("SetupOperand32Bit operand error: %s" % (x))


def ConvertAdd(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " + "
        + source2
        + ";\n"
        + SaveToOperand32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < "
        + oldDest
        + " ? 1:1 : 0:1;\n"
        + "cf_part2:1 = "
        + dest
        + " < "
        + source1
        + " ? 1:1 : 0:1;\n"
        + "cf_part3:1 = "
        + dest
        + " < "
        + source2
        + " ? 1:1 : 0:1;\n"
        + "cf:1 = cf_part1:1 | cf_part2:1 | cf_part3:1;\n"
        + "of_part1:1 = split("
        + oldDest
        + ", 31, 31) == split("
        + source1
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part2:1 = split("
        + source1
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part3:1 = split("
        + source2
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of:1 = of_part1:1 & of_part2:1 & of_part3:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )

    return dslparse.dslToAst(tempString)


def ConvertAddI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " + "
        + source2
        + ";\n"
        + SaveToOperand32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < "
        + oldDest
        + " ? 1:1 : 0:1;\n"
        + "cf_part2:1 = "
        + dest
        + " < "
        + source1
        + " ? 1:1 : 0:1;\n"
        + "cf_part3:1 = "
        + dest
        + " < "
        + source2
        + " ? 1:1 : 0:1;\n"
        + "cf:1 = cf_part1:1 | cf_part2:1 | cf_part3:1;\n"
        + "of_part1:1 = split("
        + oldDest
        + ", 31, 31) == split("
        + source1
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part2:1 = split("
        + source1
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part3:1 = split("
        + source2
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of:1 = of_part1:1 & of_part2:1 & of_part3:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )

    return dslparse.dslToAst(tempString)


def ConvertSub(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " - "
        + source2
        + ";\n"
        + SaveToOperand32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < "
        + oldDest
        + " ? 1:1 : 0:1;\n"
        + "cf_part2:1 = "
        + dest
        + " < "
        + source1
        + " ? 1:1 : 0:1;\n"
        + "cf_part3:1 = "
        + dest
        + " < "
        + source2
        + " ? 1:1 : 0:1;\n"
        + "cf:1 = cf_part1:1 | cf_part2:1 | cf_part3:1;\n"
        + "of_part1:1 = split("
        + oldDest
        + ", 31, 31) == split("
        + source1
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part2:1 = split("
        + source1
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part3:1 = split("
        + source2
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of:1 = of_part1:1 & of_part2:1 & of_part3:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )

    return dslparse.dslToAst(tempString)


def ConvertSubI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " - "
        + source2
        + ";\n"
        + SaveToOperand32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < "
        + oldDest
        + " ? 1:1 : 0:1;\n"
        + "cf_part2:1 = "
        + dest
        + " < "
        + source1
        + " ? 1:1 : 0:1;\n"
        + "cf_part3:1 = "
        + dest
        + " < "
        + source2
        + " ? 1:1 : 0:1;\n"
        + "cf:1 = cf_part1:1 | cf_part2:1 | cf_part3:1;\n"
        + "of_part1:1 = split("
        + oldDest
        + ", 31, 31) == split("
        + source1
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part2:1 = split("
        + source1
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of_part3:1 = split("
        + source2
        + ", 31, 31) != split("
        + dest
        + ", 31, 31) ? 1:1 : 0:1;\n"
        + "of:1 = of_part1:1 & of_part2:1 & of_part3:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )

    return dslparse.dslToAst(tempString)


def ConvertOr(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " | "
        + source2
        + ";\n"
        + SaveToOperand32BitRegister(x, source1, source2, dest, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertOrI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " | "
        + source2
        + ";\n"
        + SaveToOperand32BitImmediate(x, source1, source2, dest, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertAnd(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " & "
        + source2
        + ";\n"
        + SaveToOperand32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertAndI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " & "
        + source2
        + ";\n"
        + SaveToOperand32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertXor(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " ^ "
        + source2
        + ";\n"
        + SaveToOperand32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertXorI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " ^ "
        + source2
        + ";\n"
        + SaveToOperand32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf:1 = 0:1;\n"
        + "of:1 = 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )
    return dslparse.dslToAst(tempString)


def ConvertShrI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperandForShifts32BitImmediate(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " >> "
        + source2
        + ";\n"
        + SaveToOperandForShifts32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add Flags
    if int(x[3], 0) == 1:
        tempString = tempString + "of:1 = split(" + dest + ", 31, 31) ^ split(" + dest + ", 30, 30);\n"
    else:
        tempString = tempString + "of:1 = builtin_undef;\n"
    tempString = tempString + (
        "cf:1 = split("
        + dest
        + ", 31, 31);\n"
        + "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "sf:1 = split("
        + dest
        + ", 31, 31);\n"
    )

    return dslparse.dslToAst(tempString)


def ConvertShlI(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperandForShifts32BitImmediate(x)
    tempString = tempString + (
        dest
        + " = "
        + source1
        + " << "
        + source2
        + ";\n"
        + SaveToOperandForShifts32BitImmediate(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    tempString = tempString + "cf:1 = split(" + dest + ", 0, 0);\n"
    if int(x[3], 0) == 1:
        tempString = tempString + "of:1 = split(" + dest + ", 31, 31) ^ cf:1;\n"
    else:
        tempString = tempString + "of:1 = builtin_undef;\n"
    tempString = tempString + ("zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n" + "sf:1 = split(" + dest + ", 31, 31);\n")
    return dslparse.dslToAst(tempString)


def ConvertShr(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperandForShifts32BitRegister(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " >> "
        + source2
        + ";\n"
        + SaveToOperandForShifts32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # Add flags
    # if int(x[3], 0) == 1:
    #     tempString = tempString + "of:1 = split(" + oldDest + ", 31, 31);\n"
    # else:
    #     tempString = tempString + "of:1 = builtin_undef;\n"
    # tempString = tempString + (
    #     "cf:1 = split("
    #     + oldDest
    #     + ", "
    #     + str(int(x[3], 0) - 1)
    #     + ", "
    #     + str(int(x[3], 0) - 1)
    #     + ");\n"
    #     + "zf:1 = "
    #     + dest
    #     + " == 0 ? 1:1 : 0:1;\n"
    #     + "sf:1 = split("
    #     + dest
    #     + ", 31, 31);\n"
    # )
    return dslparse.dslToAst(tempString)


def ConvertShl(x):
    dest, source1, source2, oldDest, addr, tempString = SetupOperandForShifts32BitRegister(x)
    tempString = tempString + (
        oldDest
        + " = "
        + dest
        + ";\n"
        + dest
        + " = "
        + source1
        + " << "
        + source2
        + ";\n"
        + SaveToOperandForShifts32BitRegister(x, dest, source1, source2, oldDest, addr)
    )

    # # Add flags
    # tempString = tempString + "cf:1 = split(" + dest + ", 31, 31);\n"
    # if int(x[3], 0) == 1:
    #     tempString = tempString + "of:1 = split(" + dest + ", 31, 31) ^ cf:1;\n"
    # else:
    #     tempString = tempString + "of:1 = builtin_undef;\n"
    # tempString = tempString + ("zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n" + "sf:1 = split(" + dest + ", 31, 31);\n")
    return dslparse.dslToAst(tempString)


def ConvertLoad(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (dest + " = " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertLoadI(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (dest + " = " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertBranchEqual(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (dest + " == " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertBranchNotEqual(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (dest + " != " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertBranchGreaterEqual(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (dest + " >= " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertBranchLess(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    tempString = tempString + (dest + " < " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertJump(x):
    destList, tempString = ConvertOperand(x[1])
    dest = destList[0]
    tempString = "jmp 1:1 == 1:1 ? " + dest + ";"
    jmpAst = dslparse.dslToAst(tempString)
    return jmpAst


# def ConvertJnz(x) :
#     destList, tempString = ConvertOperand(x[1])
#     dest = destList[0]
#     tempString = tempString + "jmp zf:1 == 0:1 ? " + dest + " : L$NONE;"

#     jnzAst = dslparse.dslToAst(tempString)
#     return jnzAst

# def ConvertJz(x) :
#     destList, tempString = ConvertOperand(x[1])
#     dest = destList[0]
#     tempString = "jmp zf:1 == 1:1 ? " + dest + " : L$NONE;"

#     jzAst= dslparse.dslToAst(tempString)
#     return jzAst

# def ConvertJmp(x) :
#     destList, tempString = ConvertOperand(x[1])
#     dest = destList[0]
#     tempString = "jmp 1:1 == 1:1 ? " + dest + " : L$NONE;"

#     jmpAst = dslparse.dslToAst(tempString)
#     return jmpAst


def ConvertAddw(x):
    sys.exit("Please implement Convert for: %s" % (x))


def ConvertSubw(x):
    sys.exit("Please implement Convert for: %s" % (x))


def ConvertDefault(x):
    sys.exit("Please implement Convert for: %s" % (x))


def ConvertToDsl(RISCVInsts):
    retList = []
    for RISCVI in RISCVInsts:
        if len(RISCVI) == 4:
            if RISCVI[1] == "x0":
                sys.exit("x0 cannot be used as destination register")
            if RISCVI[2] == "x0":
                RISCVI[2] = "0"
            if RISCVI[3] == "x0":
                RISCVI[3] = "0"
            convFunc = convertSwitcherBinary.get(RISCVI[0], ConvertDefault)
        if len(RISCVI) == 3:
            if RISCVI[1] == "x0":
                sys.exit("x0 cannot be used as destination register")
            if RISCVI[2] == "x0":
                RISCVI[2] = "0"
            convFunc = convertSwitcherUnary.get(RISCVI[0], ConvertDefault)
        if len(RISCVI) == 2:
            if Is32Register(RISCVI):
                sys.exit("needs to be a label, label always start with L here")
            if isImmediate(RISCVI):
                sys.exit("needs to be a label, label always start with L here")
            convFunc = convertSwitcherJump.get(RISCVI[0], ConvertDefault)
        insts = convFunc(RISCVI)
        retList.extend(insts)

    return retList


convertSwitcherJump = {
    "jmp": ConvertJump,
}
convertSwitcherUnary = {
    "ld": ConvertLoad,
    "li": ConvertLoadI,
    "beq": ConvertBranchEqual,
    "bne": ConvertBranchNotEqual,
    "bge": ConvertBranchGreaterEqual,
    "blt": ConvertBranchLess,
}

convertSwitcherBinary = {
    "add": ConvertAdd,
    "sub": ConvertSub,
    "or": ConvertOr,
    "and": ConvertAnd,
    "xor": ConvertXor,
    "addi": ConvertAddI,
    "subi": ConvertSubI,
    "ori": ConvertOrI,
    "andi": ConvertAndI,
    "xori": ConvertXorI,
    "srli": ConvertShrI,
    "slli": ConvertShlI,
    "srl": ConvertShr,
    "sll": ConvertShl,
}
