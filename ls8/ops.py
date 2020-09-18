import sys
class Ops:
    def __init__(self):
        self.codes = {}
        self.codes[160] = self.oper_ADD
        self.codes[161] = self.oper_SUB
        self.codes[162] = self.oper_MUL
        self.codes[163] = self.oper_DIV
        self.codes[164] = self.oper_MOD
        self.codes[101] = self.oper_INC
        self.codes[102] = self.oper_DEC
        self.codes[167] = self.oper_CMP
        self.codes[168] = self.oper_AND
        self.codes[105] = self.oper_NOT
        self.codes[170] = self.oper_OR
        self.codes[171] = self.oper_XOR
        self.codes[172] = self.oper_SHL
        self.codes[173] = self.oper_SHR
        self.codes[80] = self.oper_CALL
        self.codes[17] = self.oper_RET
        self.codes[82] = self.oper_INT
        self.codes[19] = self.oper_IRET
        self.codes[84] = self.oper_JMP
        self.codes[85] = self.oper_JEQ
        self.codes[86] = self.oper_JNE
        self.codes[87] = self.oper_JGT
        self.codes[88] = self.oper_JLT
        self.codes[89] = self.oper_JLE
        self.codes[90] = self.oper_JGE
        self.codes[0] = self.oper_NOP
        self.codes[1] = self.oper_HLT
        self.codes[130] = self.oper_LDI
        self.codes[131] = self.oper_LD
        self.codes[132] = self.oper_ST
        self.codes[69] = self.oper_PUSH
        self.codes[70] = self.oper_POP
        self.codes[71] = self.oper_PRN
        self.codes[72] = self.oper_PRA

    def oper_ADD(self, reg_a, reg_b):
        self.ram[reg_a] += self.ram[reg_b]
    def oper_SUB(self, reg_a, reg_b):
        self.ram[reg_a] -= self.ram[reg_b]
    def oper_MUL(self, reg_a, reg_b):
        self.ram[reg_a] *= self.ram[reg_b]
    def oper_DIV(self, reg_a, reg_b):
        self.ram[reg_a] /= self.ram[reg_b]
    def oper_MOD(self, reg_a, reg_b):
        self.ram[reg_a] %= self.ram[reg_b]
    def oper_INC(self, reg_a):
        self.ram[reg_a] += 1
    def oper_DEC(self, reg_a):
        # self.ram[reg_a] -= 1
        derp = self.ram[reg_a]
        control = 1
        while ((derp & control) == False):
            derp = derp ^ control
            control = control << 1
        self.ram[reg_a] = derp ^ control
    def oper_CMP(self, reg_a, reg_b):
        self.FL &= int('11111000', 2)
        if reg_a == reg_b:
            self.FL |= int('00000001', 2)
        if reg_a < reg_b:
            self.FL |= int('00000100', 2)
        if reg_a > reg_b:
            self.FL |= int('00000010', 2)
    def oper_AND(self, reg_a, reg_b):
        self.ram[reg_a] &= reg_b
    def oper_NOT(self, reg_a):
        self.ram[reg_a] = 255 - self.ram[reg_a]
    def oper_OR(self, reg_a, reg_b):
        self.ram[reg_a] |= self.ram[reg_b]
    def oper_XOR(self, reg_a, reg_b):
        self.ram[reg_a] ^= self.ram[reg_b]
    def oper_SHL(self, reg_a, reg_b):
        shl_val = self.ram[reg_a] << self.ram[reg_b]
        self.ram[reg_a] = shl_val & 255 
    def oper_SHR(self, reg_a, reg_b):
        self.ram[reg_a] >>= self.ram[reg_b] 
    def oper_CALL(self, reg_a):
        self.stack_p -= 1
        self.ram[self.stack_p] = self.PC + 1
        self.PC = self.ram[reg_a]
    def oper_RET(self):
        ret_reg = self.ram[self.stack_p]
        self.stack_p += 1
        self.PC = ret_reg - 1
    def oper_INT(self):
        pass
    def oper_IRET(self):
        pass
    def oper_JMP(self, reg_a):
        self.PC = self.ram[reg_a]
    def oper_JEQ(self, reg_a):
        if self.FL & 1 == 1:
            self.PC = self.ram[reg_a]
    def oper_JNE(self, reg_a):
        if self.FL & 1 != 1:
            self.PC = self.ram[reg_a]
    def oper_JGT(self, reg_a):
        if self.FL & 2 == 2:
            self.PC = self.ram[reg_a]
    def oper_JLT(self, reg_a):
        if self.FL & 4 == 4:
            self.PC = self.ram[reg_a]
    def oper_JLE(self, reg_a):
        if self.FL & 5 in [1, 4]:
            self.PC = self.ram[reg_a]
    def oper_JGE(self, reg_a):
        if self.FL & 3 in [1, 2]:
            self.PC = self.ram[reg_a]
    def oper_NOP(self):
        pass
    def oper_HLT(self):
        sys.exit()
    def oper_LDI(self, reg_a, num):
        self.ram[reg_a] = num
    def oper_LD(self, reg_a, reg_b):
        addy = self.ram[reg_b]
        self.ram[reg_a] = self.ram[addy]
    def oper_ST(self, reg_a, reg_b):
        addy = self.ram[reg_a]
        self.ram[reg_b] = self.ram[addy]
    def oper_PUSH(self, reg_a):
        # print(f'pushing {self.ram[reg_a]} to index {self.stack_p} + 1')
        self.stack_p -= 1
        self.ram[self.stack_p] = self.ram[reg_a]
        # print(f'pushed {self.ram[reg_a]} to index {self.stack_p}')
    def oper_POP(self, reg_a):
        self.ram[reg_a] = self.ram[self.stack_p]
        self.stack_p += 1
    def oper_PRN(self, reg_a):
        print(self.ram[reg_a])
    def oper_PRA(self, reg_a):
        print(chr(reg_a))
