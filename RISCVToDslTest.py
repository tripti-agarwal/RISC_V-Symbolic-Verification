import riscvparse
import riscvtodsl

test1 = "ld x1, 8(x2)"

test = test1
insts = riscvparse.RISCVParse(test)
print("insts:")
print(insts)
dsl = riscvtodsl.ConvertToDsl(insts)
print("dsl:")
print(dsl)

print(f"d in dsl:")
for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
