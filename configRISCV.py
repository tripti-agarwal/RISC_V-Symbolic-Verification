# General
verbose = False  # message verbosity
memModel = 32  # memory model uses 32-bit value model.
smtTimeout = 1000 * 60 * 5  # 5 minute
aliasAnalysis = True  # Performs alias analysis to reduce memory read nodes.
tempQueryFile = "temp.z3"  # This is where we will save query for bash z3.
p1File = None  # File for p1
p2File = None  # File for p2
z3CheckSatCommand = "(check-sat-using default)"
currentUnknownCount = 0
maxUnknownCount = 1
gout = None

# For statistics
totalNodesToCompare = 0
equivNodeNum = 0
noEquivNodeNum = 0
readNodeNum = 0
indexAliasNum = 0
totalIndexAliasNum = 0
totalSmtTime = 0
totalAliasAnalysisTime = 0
totalVerificationTime = 0
analysisStartTime = 0
analysisEndTime = 0


def PrintStatistics():
    print("Total Time : %f" % (analysisEndTime - analysisStartTime))
    print("Amount of Time Spent Verifying : %f" % (totalVerificationTime))
    # print("Amount of Time Spent Alias Analysis : %f" % (totalAliasAnalysisTime))
    # print("Amount of Time Spent doing SMT Query : %f" % (totalSmtTime))
    print("Total Number of Node Pairs to Compare : %d" % (totalNodesToCompare))
    print("Number of Equivalent Pairs of Nodes : %d" % (equivNodeNum))
    # print("Number of Not Equivalent Pair of Nodes : %d" % (noEquivNodeNum))
    print("Number of Array Read Nodes Reduced : %d" % (readNodeNum))
    # print("Number of Array Index Comparisons: %d" % (totalIndexAliasNum))


def PrintGout(message):
    if gout != None:
        file = open(gout, "w")
        # First line is the message = result of analysis
        file.write(message)
        file.write("\n")
        # Second line is how long it took total
        file.write("Total Time :%f\n" % (analysisEndTime - analysisStartTime))
        # Third line is Amount of Time Spent Verifying
        file.write("Amount of Time Spent Verifying :%f\n" % (totalVerificationTime))
        file.close()


# Language for p1 and p2. This is used primarily for parsing the file. Once the files are parsed,
# everything is the same. By default, we assume p1 is dsl and p2 is asm.
p1lang = 0
p2lang = 1
plangDict = {"dsl": 0, "asm": 1}
plangDictRev = {0: "dsl", 1: "asm"}


def ProgLangArgToProgLangCode(arg):
    if arg.lower() in plangDict:
        return plangDict[arg.lower()]
    return None


# Static function that sets up config. Just in case I may need multiple configuration...
def SetUpConfig(c, arg):
    # Set verbosity
    c.verbose = arg.verbose

    error_exit = False
    # Set p1 and p2 file :
    if arg.p1 == None:
        print("Command Argument Error: Please provide file for p1")
        error_exit = True
    else:
        print("\n p1 arg=", arg.p1)
        c.p1File = arg.p1
    if arg.p2 == None:
        print("Command Argument Error: Please provide file for p2")
        error_exit = True
    else:
        c.p2File = arg.p2

    # Set p1lang and p2lang (How to parse p1 and p2 file? DSL or ASM?) :
    if arg.p1lang == None:
        print("Command Argument Warning: p1lang not specified. Assuming p1 is DSL")
        c.p1lang = 0
    else:
        p1langCode = ProgLangArgToProgLangCode(arg.p1lang)
        if p1langCode == None:
            print("Command Argument Error: Unknown p1lang code: %s" % (arg.p1lang))
            error_exit = True
        c.p1lang = p1langCode

    if arg.p2lang == None:
        print("Command Argument Warning: p2lang not specified. Assuming p2 is ASM")
        c.p2lang = 1
    else:
        p2langCode = ProgLangArgToProgLangCode(arg.p2lang)
        if p2langCode == None:
            print("Command Argument Error: Unknown p2lang code: %s" % (arg.p1lang))
            error_exit = True
        else:
            c.p2lang = p2langCode

    if error_exit:
        assert False

    # Set gout
    if arg.gout != None:
        c.gout = arg.gout
