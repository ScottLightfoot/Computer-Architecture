#!/usr/bin/env python3

import sys
from cpu import *

cpu = CPU()

pgm1 = './examples/call.ls8'
pgm2 = './examples/interrupts.ls8'
pgm3 = './examples/keyboard.ls8'
pgm4 = './examples/mult.ls8'
pgm5 = './examples/print8.ls8'
pgm6 = './examples/printstr.ls8'
pgm7 = './examples/sctest.ls8'
pgm8 = './examples/stack.ls8'
pgm9 = './examples/stackoverflow.ls8'

cpu.load(pgm6)

cpu.run()