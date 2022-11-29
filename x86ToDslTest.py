import x86parse
import x86todsl8bit

test = "andl $1, %ebx"
# test = "movl    %edi, -4(%rbp)"
# test = "movq    %rsp, %rbp"
# test = "movl    -4(%rbp), %eax"
# test = "imull   -4(%rbp), %eax"
# test = "popq    %rbp"

insts = x86parse.ASMToX86Parse(test)
print(insts)
dsl = x86todsl8bit.ConvertToDsl(insts)
for d in dsl:
    d.SetProgramOrigin("P", False)
    print(d.ToString())
