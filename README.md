# a202
# 2 BIT CPU Emulator for VoxelCore


## Instructions

*RR - register*
*DD - imm data*
*RP - register pair*

- NOP 00 - none
- LDM DD - Load data to Acc
- SWP RR - Swipe Acc and R[0-3]
- ADD RR - Add data from reg to Acc
- JUN RP - Jump Unconditional, Addr from R0:R1 rp = 0 or R2:R3 rp = 1
- JC RP  - Ju,p if Carry, Addr from R0:R1 rp = 0 or R2:R3 rp = 1
- OUT DD - Transfer Data from Acc to port [imm value]

## Registers

- Acc - main register [2-bit]
- r0 - [2-bit]
- r1 - [2-bit]
- r2 - [2-bit]
- r3 - [2-bit]
- pc - [6-bit]

## Flags

- C - carry flag
- Z - zero flag (not used)

## Instruction format

**Base instruction:**

`opc opr` - `xx yy` [4-bit]
LDM: 01 DD
SWP: 10 RR

**Extended instruction:**
*All extended instructions starts with 11*

`ext opc opr` - `11 xx yy` [6-bit]
ADD: 11 00 RR
JUN: 11 01 RP
JC:  11 10 RP
OUT: 11 11 DD



