import riscvparse
import riscvtodsl

test1 = "srli x3, x4, $50"

test = test1
insts = riscvparse.RISCVParse(test)
print(insts)
dsl = riscvtodsl.ConvertToDsl(insts)
print(dsl)

for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
