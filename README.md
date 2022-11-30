

## SymDiff_RISC-V
This tool is is built on top of CASM-Verify [Automatic Equivalence Checking for Assembly Implementations of Cryptography Libraries @ CGO 2019](https://www.cs.rutgers.edu/~santosh.nagarakatte/papers/cgo19-casmverify-preprint.pdf) and can perform verification of optimized RISC-V pro-
grams to DSL programs or other RISC-V programs, given the precondition and postcondition https://www.overleaf.com/read/kdrjyvzgsqys.  

## Prerequisite
The tool requires python3 and the z3 bindings for python3. In ubuntu, the requirements can be installed using the following commands:
```bash
$ sudo apt-get install python3 python3-pip
$ sudo python3 -m pip install z3-solver
```
In macOS, use homebrew instead of apt-get:
```bash
$ brew install python3
$ sudo python3 -m pip install z3-solver
```

To install [z3](https://github.com/Z3Prover/z3) manually instead of using python package manager, follow the instruction in the link provided: [z3](https://github.com/Z3Prover/z3)


### Manual Installation
To manually install CASM-Verify, install the [prerequisites](https://github.com/rutgers-apl/CASM-Verify/blob/master/README.md#prerequisite) and clone this repository:
```bash
https://github.com/tripti-agarwal/RISC_V-Symbolic-Verification.git
```
Now you're ready to use SymDiff_RISC-V.


## Usage
For the rest of the readme, we will be using the example in test/RISCV_test6 unless otherwise specified.

To verify the assembly implementation(test/sha2rnd/asm) using CASM-Verify, use the following command:
```bash
python3 main_RISCV.py --pre test/RISCV_test7/pre --post test/RISCV_test7/post --p1 test/RISCV_test7/p1 --p1lang asm --p2 test/RISCV_test7/p2 --p2lang asm
```
There are seven important parameters:
  1) --p1: specifies the file path to the reference implementation.
  2) --p1lang: specifies whether the reference implementation is written in x86_64 assembly (asm) or in our DSL (dsl).
  3) --p2: specifies the file path to the target implementation.
  4) --p2lang: specifies whether the target implementation is written in x86_64 assembly (asm) or in our DSL (dsl).
  5) --pre: File containing the precondition that specifies the program state at the beginning of p1 and p2.
  6) --post: File containing the postcondition that specifies which variables have to be equivalent for p1 and p2 to be equivalent.
  
The above example (test/RISCV_test6) verifies an assembly implementation against the reference implementation written in our DSL, using a 32-bit value memory model.



## Details

### Assembly Implementations
<details><summary>Click to see details</summary>
<p>

SymDiff_RISC-V accepts RISC-V syntax of assembly instructions. 

</p>
</details>




