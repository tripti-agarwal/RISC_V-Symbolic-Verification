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
