import riscvparse
import riscvtodsl

test = "xor  x10, x2, x3"

insts = riscvparse.RISCVParse(test)
print(insts)
dsl = riscvtodsl.ConvertToDsl(insts)
print(dsl)

for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
