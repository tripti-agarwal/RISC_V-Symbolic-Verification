import riscvparse
import riscvtodsl

test = "srli x2, x3, $1"

insts = riscvparse.RISCVParse(test)
print(insts)
dsl = riscvtodsl.ConvertToDsl(insts)
print(dsl)

for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
