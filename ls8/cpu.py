"""CPU functionality."""

import sys
from time import time
from ops import Ops


class CPU(Ops):
    """Main CPU class."""

    def __init__(self, memory = 256, regs = 8):
        '''
        Internal Registers:
        (??? Reserved registers 0-4 ???)
        PC (program counter)
        IR (instruction register)
        MAR (memory address register)
        MDR (memory dump register)
        FL (flags)
        
        Reserved Registers:
        0 -
        1 -
        2 -
        3 -
        4 -
        5 - Interrupt Mask
        6 - Interrupt Stack
        7 - Stack Pointer
        '''
        self.reg = [0] * (regs - 3)
        self.ram = [0] * memory
        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0
        self.IM = 0 
        self.IS = 0
        self.stack_p = 244
        super().__init__()

    
    def ram_read(self, addy):
        return self.ram[addy]


    def ram_write(self, addy, val):
        self.ram[addy] = val


    def load(self, prog = None):
        """Load a program into memory."""

        if prog == None:
            print('\nTry again.\nTry harder.\n\n')
            return

        address = 0
        with open(prog) as f:
            for line in f:
                l = line.split('#')[0].strip()
                if l == '':
                    continue
                try:
                    i = int(l, 2)
                except Exception:
                    print('\nTry again.\nTry harder.')
                    sys.exit('derp')
                self.ram[address] = i
                address += 1


    def run(self):
        """Run the CPU."""
        self.t = time()
        while True:
            if time() - self.t >= 1:
                self.IS |= 1
            self.IM &= self.IS
            if self.IM > 0:
                i = 1
                while((self.IM & i) == False):
                    self.IM = self.IM ^ i
                    i = i << 1
                self.stack_p -= 1
                self.ram[self.stack_p] = self.PC
                self.stack_p -= 1
                self.ram[self.stack_p] = self.FL

            self.IR = self.ram[self.PC]
            op_count = self.IR >> 6
            self.PC += 1
            # print(self.codes[self.IR])
            # breakpoint()

            if op_count == 1:
                self.MAR = self.ram[self.PC]
                if self.IR & 8 != 8:
                    self.PC += 1
                self.codes[self.IR](self.MAR)

            elif op_count == 2:
                self.MAR = self.ram_read(self.PC)
                self.PC += 1
                self.MDR = self.ram_read(self.PC)
                self.PC += 1
                self.codes[self.IR](self.MAR, self.MDR)

            else:
                self.codes[self.IR]()
