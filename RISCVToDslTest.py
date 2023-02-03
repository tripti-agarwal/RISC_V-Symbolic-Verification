import riscvparse
import riscvtodsl

test = "xori x7, x7, $-1 "

insts = riscvparse.RISCVParse(test)
print(insts)
dsl = riscvtodsl.ConvertToDsl(insts)
print(dsl)

for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
