from Parser import Parser
from Lexer import Lexer
from CodeGen import CodeGenContext

import sys

# ========================
# =  ARTI 202 ASSEMBLER  =
# ========================

class Assembler:
    def __init__(self, filename, outf):
        self.outf = outf
        with open(filename, "r") as f:
            self.src = f.read()
            
        
    def assemble(self):
        self.lexer = Lexer(self.src)
        self.ctx = CodeGenContext(self.outf)
        self.parser = Parser(self.lexer, self.ctx)
        
        bin_code = self.parser.parse()
        
        print(self.ctx.BIN_CODE)
        
        
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py input.asm output.bin")
        sys.exit(1)
    
    asm = Assembler(sys.argv[1], sys.argv[2])
    asm.assemble()