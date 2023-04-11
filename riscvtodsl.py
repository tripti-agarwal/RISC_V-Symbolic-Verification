import sys


from RISCVtodslHelper import *
import config
import dslparse
import dslinstructions


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

        if Is32Register(x[1]) and (Is32Register(x[2])):
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
        elif Is32Register(x[1]) and IsMemory(x[2]):
            if (x[0] == "ld"): # is a load instruction
                dest = x[1]
                source = x[2]
                addr = ""
                return dest, source, oldDest, addr, tempString


def SetupOperand32BitImmediate(x):
    oldDest = "oldDest"
    tempString = ""
    dest = x[1]
    addr = ""
    if len(x) == 4:
        if Is32Register(x[1]) and (Is32Register(x[2]) or isImmediate(x[3])):
            source1 = x[2]
            source2 = x[3]

            return dest, source1, source2, oldDest, addr, tempString

        if Is32Register(x[1]) and (isImmediate(x[2]) or isImmediate(x[3])):

            source1 = x[2]
            source2 = x[3]

            return dest, source1, source2, oldDest, addr, tempString

        if Is32Register(x[1]) and (isImmediate(x[2]) or Is32Register(x[3])):

            source1 = x[2]
            source2 = x[3]

            return dest, source1, source2, oldDest, addr, tempString

    if len(x) == 3:
        if Is32Register(x[1]) and isImmediate(x[2]):

            source = x[2]

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


def ConvertCmpl(x):
    # Right side - left side.
    # 32 bit cmp operation
    sourceList, tempString = ConvertOperand(x[2])
    source = sourceList[0]
    destList, tempString = ConvertOperand(x[3], tempString)
    dest = destList[0]
    tempString = tempString + "temp = " + dest + " - " + source + ";\n"
    # zf
    tempString = tempString + "zf:1 = temp == 0 ? 1:1 : 0:1;\n"
    # of : (left side sign bit) != (right side sign bit) and (right side sign bit) == (result sign bit)
    tempString = tempString + "of_part1:1 = split(" + source + ", 31, 31) != split(" + dest + ", 31, 31) ? 1:1 : 0:1;\n"
    tempString = tempString + "of_part2:1 = split(" + dest + ", 31, 31) == split(temp, 31, 31) ? 1:1 : 0:1;\n"
    tempString = tempString + "of:1 = of_part1:1 & of_part2:1;\n"
    # cf : most significant bit requires carry if source is greater than dest.
    tempString = tempString + "cf:1 = " + source + " > " + dest + " ? 1:1 : 0:1;\n"
    # sf
    tempString = tempString + "sf:1 = split(temp, 31, 31);\n"

    cmpAst = dslparse.dslToAst(tempString)
    return cmpAst


def ConvertAdd(x):
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + "oldDest = " + dest + ";\n"
    tempString = tempString + dest + " = " + source1 + " + " + source2 + ";\n"

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < oldDest? 1:1 : 0:1;\n"
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
        + "of_part1:1 = split(oldDest, 31, 31) == split("
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
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + "oldDest = " + dest + ";\n"
    tempString = tempString + dest + " = " + source1 + " + " + source2 + ";\n"

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < oldDest? 1:1 : 0:1;\n"
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
        + "of_part1:1 = split(oldDest, 31, 31) == split("
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
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + "oldDest = " + dest + ";\n"
    tempString = tempString + dest + " = " + source1 + " - " + source2 + ";\n"

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < oldDest? 1:1 : 0:1;\n"
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
        + "of_part1:1 = split(oldDest, 31, 31) == split("
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
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + "oldDest = " + dest + ";\n"
    tempString = tempString + dest + " = " + source1 + " - " + source2 + ";\n"

    # Add flags
    tempString = tempString + (
        "zf:1 = "
        + dest
        + " == 0 ? 1:1 : 0:1;\n"
        + "cf_part1:1 = "
        + dest
        + " < oldDest? 1:1 : 0:1;\n"
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
        + "of_part1:1 = split(oldDest, 31, 31) == split("
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
    # 32 bit or operation
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " | " + source2 + ";\n"

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
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " | " + source2 + ";\n"

    # zf : dest == 0
    tempString = tempString + "zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n"
    # cf : 0
    tempString = tempString + "cf:1 = 0:1;\n"
    # of : 0
    tempString = tempString + "of:1 = 0:1;\n"
    # sf : most significant bit of dest
    tempString = tempString + "sf:1 = split(" + dest + ", 31, 31);\n"

    orAst = dslparse.dslToAst(tempString)
    return orAst


def ConvertAnd(x):
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " & " + source2 + ";\n"

    # zf : dest == 0
    tempString = tempString + "zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n"
    # cf : 0
    tempString = tempString + "cf:1 = 0:1;\n"
    # of : 0
    tempString = tempString + "of:1 = 0:1;\n"
    # sf : most significant bit of dest
    tempString = tempString + "sf:1 = split(" + dest + ", 31, 31);\n"

    andAst = dslparse.dslToAst(tempString)
    return andAst


def ConvertAndI(x):
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " & " + source2 + ";\n"

    # zf : dest == 0
    tempString = tempString + "zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n"
    # cf : 0
    tempString = tempString + "cf:1 = 0:1;\n"
    # of : 0
    tempString = tempString + "of:1 = 0:1;\n"
    # sf : most significant bit of dest
    tempString = tempString + "sf:1 = split(" + dest + ", 31, 31);\n"

    andAst = dslparse.dslToAst(tempString)
    return andAst


def ConvertXor(x):
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " ^ " + source2 + ";\n"

    # zf : dest == 0
    tempString = tempString + "zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n"
    # cf : 0
    tempString = tempString + "cf:1 = 0:1;\n"
    # of : 0
    tempString = tempString + "of:1 = 0:1;\n"
    # sf : most significant bit of dest
    tempString = tempString + "sf:1 = split(" + dest + ", 31, 31);\n"

    xorAst = dslparse.dslToAst(tempString)
    return xorAst


def ConvertXorI(x):
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]

    sourceList2, tempString = ConvertOperand(x[3], tempString)
    source2 = sourceList2[0]

    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]

    tempString = tempString + dest + " = " + source1 + " ^ " + source2 + ";\n"

    # zf : dest == 0
    tempString = tempString + "zf:1 = " + dest + " == 0 ? 1:1 : 0:1;\n"
    # cf : 0
    tempString = tempString + "cf:1 = 0:1;\n"
    # of : 0
    tempString = tempString + "of:1 = 0:1;\n"
    # sf : most significant bit of dest
    tempString = tempString + "sf:1 = split(" + dest + ", 31, 31);\n"

    xorAst = dslparse.dslToAst(tempString)
    return xorAst


def ConvertShrI(x):
    # 32 bit rotate right operation
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]
    sourceList2, tempString = ConvertOperand(x[3])
    source2 = sourceList2[0]
    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]
    tempString = tempString + dest + " = " + source1 + " >> " + source2 + ";\n"

    # cf : least significant bit of destination
    tempString = (
        tempString
        + "cf:1 = split(oldDest, "
        + str((int(source2, 0) - 1) % 32)
        + ", "
        + str((int(source2, 0) - 1) % 32)
        + ");\n"
    )
    # of : if source == 1, most significant bit of old destination
    sourceVal = int(x[3], 0)
    if sourceVal == 1:
        tempString = tempString + "of:1 = split(oldDest, 31, 31);\n"
    else:
        tempString = tempString + "of:1 = builtin_undef;\n"

    shrAst = dslparse.dslToAst(tempString)
    return shrAst


def ConvertShlI(x):
    # 32 bit rotate left operation
    sourceList1, tempString = ConvertOperand(x[2])
    source1 = sourceList1[0]
    sourceList2, tempString = ConvertOperand(x[3])
    source2 = sourceList2[0]
    destList, tempString = ConvertOperand(x[1], tempString)
    dest = destList[0]
    tempString = tempString + dest + " = " + source1 + " << " + source2 + ";\n"

    # cf : least significant bit of destination
    tempString = (
        tempString
        + "cf:1 = split(oldDest, "
        + str((int(source2, 0) + 1) % 32)
        + ", "
        + str((int(source2, 0) + 1) % 32)
        + ");\n"
    )
    # of : if source == 1, then of = the xor of the most significant bit and cf
    sourceVal = int(x[3], 0)
    if sourceVal == 1:
        tempString = tempString + "of:1 = split(" + dest + ", 31, 31) ^ cf:1;\n"
    else:
        tempString = tempString + "of:1 = builtin_undef;\n"

    shllAst = dslparse.dslToAst(tempString)
    return shllAst


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
        + " >>> "
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
        + " <<< "
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
    if IsMemory(source) or IsMemory(dest):
        sourceList, tempString = ConvertOperand(x[2])
        source = sourceList[0]
        destList, tempString = ConvertOperand(x[1], tempString)
        dest = destList[0]
        tempString = tempString + dest + " = " + source + ";\n"
    else:
        tempString = tempString + (
            dest + " = " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr)
        )
    return dslparse.dslToAst(tempString)


def ConvertLoadI(x):
    dest, source, oldDest, addr, tempString = SetupOperand32BitImmediate(x)
    tempString = tempString + (dest + " = " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return dslparse.dslToAst(tempString)


def ConvertBranchEqual(x):
    # dest, source, oldDest, addr, tempString = SetupOperand32BitRegister(x)
    # tempString = tempString + (dest + " == " + source + ";\n" + SaveToOperand32BitUnary(x, dest, source, oldDest, addr))
    return ConvertCmpl(x)


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
