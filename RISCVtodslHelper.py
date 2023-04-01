import pyparse.pyparsing as pp
import config
import sys

reg32 = {
    0: "x0",
    1: "x1",
    2: "x2",
    3: "x3",
    4: "x4",
    5: "x5",
    6: "x6",
    7: "x7",
    8: "x8",
    9: "x9",
    10: "x10",
    11: "x11",
    12: "x12",
    13: "x13",
    14: "x14",
    15: "x15",
    16: "x16",
    17: "x17",
    18: "x18",
    19: "x19",
    20: "x20",
    21: "x21",
    22: "x22",
    23: "x23",
    24: "x24",
    25: "x25",
    26: "x26",
    27: "x27",
    28: "x28",
    29: "x29",
    30: "x30",
    31: "x31",
}
reg32Rev = {v: k for k, v in reg32.items()}


def isImmediate(val):
    try:
        val = int(val, 0)
        return True
    except:
        return False


def Is32Register(o):
    if isinstance(o, str) and o in reg32Rev:
        return True
    return False


def IsMemory(o):
    if isinstance(o, pp.ParseResults) or isinstance(o, list):
        return True
    return False


def Get32BitRepFromRegister(o):
    if isinstance(o, str) and o in reg32Rev:
        return [o]
    else:
        sys.exit("Get32BitRepFromRegister: " + o + "is not a register I can recognize")


# Gets the correct representation of the register. Adds "bitsize" syntax as well.
def GetRegister(o, bitlength=32):
    if bitlength == 32:
        return Get32BitRepFromRegister(o)


def CalculateAddress(o):
    # ['OFFSET', 'rax']
    # ['OFFSET', 'rax', 'rdx']
    # ['OFFSET', 'rax', 'rdx', '8']
    # ['OFFSET', 'BASE', 'rdx', '8']

    assert len(o) > 1
    regSize = ":32"
    # We will always get ['OFFSET', 'BASE']
    addrString = ""
    if o[1] != "BASE":
        # Then we have base register
        baseReg = ""
        if config.Is64BitArch():
            baseReg = Get64BitRepFromRegister(o[1])[0]
        elif config.Is32BitArch():
            baseReg = Get32BitRepFromRegister(o[1])[0]
        if baseReg != "":
            addrString = addrString + baseReg

    shiftValue = 0
    if len(o) == 4:
        # Addressing mode specifies shiftValue. By definition, o[3] can only be 1, 2, 4, or 8
        if o[3] == "1":
            shiftValue = 0
        elif o[3] == "2":
            shiftValue = 1
        elif o[3] == "4":
            shiftValue = 2
        elif o[3] == "8":
            shiftValue = 3
        else:
            sys.exit("Illegal index multiplier value: %s" + (o))

    if len(o) >= 3:
        # Then we have to add additional register
        if config.Is64BitArch():
            indexReg = Get64BitRepFromRegister(o[2])[0]
        elif config.Is32BitArch():
            indexReg = Get32BitRepFromRegister(o[2])[0]

        if addrString != "":
            addrString = addrString + " + "
        if shiftValue == 0:
            addrString = addrString + indexReg
        else:
            addrString = addrString + "(" + indexReg + " << " + str(shiftValue) + regSize + ")"

    if o[0] != "OFFSET" and o[0] != "0":
        addrString = addrString + " + " + o[0] + regSize

    return addrString


def ConvertOperand(o, tempString="", bitlength=32):
    """Converts 

    Args:
        o (_type_): the register
        tempString (str, optional): . Defaults to "".
        bitlength (int, optional): _description_. Defaults to 32.

    Returns:
        _type_: _description_
    """    
    print(o)
    # This is memory addressing mode.
    if isinstance(o, pp.ParseResults) or isinstance(o, list):
        retList = []
        # Identify the bitlength of the register used for memory access.
        regSize = ":32"

        # Add base register
        taddr = o[1] + regSize

        # Add index and scale
        if len(o) == 4:
            index = o[2] + regSize
            multiplier = int(o[3])
            if multiplier == 1:
                taddr = taddr + " + " + index
            elif multiplier == 2:
                taddr = taddr + " + (" + index + " << 1" + regSize + ") "
            elif multiplier == 4:
                taddr = taddr + " + (" + index + " << 2" + regSize + ") "
            elif multiplier == 8:
                taddr = taddr + " + (" + index + " << 3" + regSize + ") "
            else:
                taddr = taddr + " + " + index

        offset = 0 if o[0] == "OFFSET" else int(o[0])
        if offset % 4 == 0:
            # Then we have no problem.
            if offset != 0:
                taddr = taddr + " + " + str(offset) + regSize
            forceSizeAdd = 0
            while forceSizeAdd < 128:
                # for example if bitlength = 32, forceSize = 128
                # we should get +0, +4, +8, and +12
                finalAddr = taddr + " + " + str(int(forceSizeAdd / 8)) + regSize
                retList.append("mem[" + finalAddr + "]")
                forceSizeAdd = forceSizeAdd + bitlength
            return retList, tempString
        else:
            # We gotta start thinking about offset memory loads.
            newoffset = int(offset / 4)
            offsetrem = offset % 4
            taddrlow = taddr if newoffset == 0 else (taddr + " + " + str(newoffset) + regSize)
            taddrhigh = (
                (taddr + " + 4" + regSize + " ") if newoffset == 0 else (taddr + " + " + str(newoffset + 4) + regSize)
            )
            forceSize = 32
            while forceSize > 0:
                forceoffset = int((forceSize - bitlength) / 8)
                if not forceoffset == 0:
                    taddrlow = taddrlow + " + " + str(forceoffset) + regSize
                    taddrhigh = taddrhigh + " + " + str(forceoffset) + regSize
                # example: 3(%r14) -> merge(split(mem[r14 + 4], 0, 23), split(mem[r14], 24, 31))
                tempString = (
                    tempString
                    + "cavtmemhigh"
                    + str(forceoffset)
                    + ":"
                    + str(offsetrem * 8)
                    + " = split(mem["
                    + taddrhigh
                    + "], 0, "
                    + str(offsetrem * 8 - 1)
                    + ");\n"
                )

                tempString = (
                    tempString
                    + "cavtmemlow"
                    + str(forceoffset)
                    + ":"
                    + str((4 - offsetrem) * 8)
                    + " = split(mem["
                    + taddrlow
                    + "], "
                    + str(offsetrem * 8)
                    + ", 31);\n"
                )

                tempString = (
                    tempString
                    + "cavtmem"
                    + str(forceoffset)
                    + " = merge(cavtmemhigh"
                    + str(forceoffset)
                    + ":"
                    + str(offsetrem * 8)
                    + ", cavtmemlow"
                    + str(forceoffset)
                    + ":"
                    + str((4 - offset) * 8)
                    + ");\n"
                )

                retList.append("cavtmem" + str(forceoffset))
                forceSize = forceSize - bitlength
            return retList, tempString
    elif o.startswith("L$"):
        return [o], tempString
    elif isImmediate(o):
        if bitlength > 32:
            return [o + ":" + str(bitlength)], tempString
        return [o], tempString
    elif o in reg32Rev:
        return GetRegister(o, bitlength), tempString
    else:
        sys.exit("I don't know what", o, "is in x86 operand.")
