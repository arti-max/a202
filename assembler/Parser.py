from dataclasses import dataclass
from typing import List, Optional
from Lexer import Lexer, Token, TokenType

class Parser:
    def __init__(self, lexer: Lexer, ctx):
        self.lexer = lexer
        self.ctx = ctx
        self.current_token = self.lexer.get_next_token()
        
        
    def error(self, message: str):
        raise SyntaxError(f"{message} at line {self.current_token.line}, column {self.current_token.column}")
    
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
            
    def parse(self) -> bin:
        while self.current_token.type != TokenType.EOF:
            print(f"{self.current_token}")
            if self.current_token.type == TokenType.INSTR:
                self.parse_instr()
            else:
                self.error(f"Unexpected token {self.current_token.type}")
                
        return self.ctx.generate()
    
    
    # DD - imm data
    # RR - register data
    # ACBR - acc buff reg
    # ACC  - Accumulator
    # RP   - register pair
    def parse_instr(self):
        print("PARSE INSTR: ",self.current_token)
        if self.current_token.value == "NOP":   # 00 00
            self.eat(TokenType.INSTR)
            self.ctx.add_bin(self.ctx.OPCODE_MAP["NOP"], 0b00)
        elif self.current_token.value == "LDM": # 01 DD
            print("LDM!")
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.NUM:
                self.ctx.add_bin(self.ctx.OPCODE_MAP["LDM"], int(self.current_token.value))
                self.eat(TokenType.NUM)
            elif self.current_token.type == TokenType.BIN:
                self.ctx.add_bin(self.ctx.OPCODE_MAP["LDM"], int(self.current_token.value))
                self.eat(TokenType.BIN)
        elif self.current_token.value == "SWP":  # 10 RR
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.REGISTER:
                self.ctx.add_bin(self.ctx.OPCODE_MAP["SWP"], self.ctx.REG_MAP[self.current_token.value])
                self.eat(TokenType.REGISTER)
        # EXTENDED
        elif self.current_token.value == "ADD": # 11 00 RR
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.REGISTER:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["ADD"], self.ctx.REG_MAP[self.current_token.value])
                self.eat(TokenType.REGISTER)     
        elif self.current_token.value == "JUN": # 11 01 RP
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.NUM:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["JUN"], int(self.current_token.value))
                self.eat(TokenType.NUM)
            elif self.current_token.type == TokenType.BIN:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["JUN"], int(self.current_token.value))
                self.eat(TokenType.BIN)
        elif self.current_token.value == "JC": # 11 10 RP
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.NUM:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["JC"], int(self.current_token.value))
                self.eat(TokenType.NUM) 
            elif self.current_token.type == TokenType.BIN:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["JC"], int(self.current_token.value))
                self.eat(TokenType.BIN)        
        elif self.current_token.value == "OUT": # 11 11 DD
            self.eat(TokenType.INSTR)
            if self.current_token.type == TokenType.NUM:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["OUT"], int(self.current_token.value))
                self.eat(TokenType.NUM)
            elif self.current_token.type == TokenType.BIN:
                self.ctx.add_bin_6(0b11, self.ctx.EXT_OPCODE_MAP["OUT"], int(self.current_token.value))
                self.eat(TokenType.BIN) 
        
         
        
        