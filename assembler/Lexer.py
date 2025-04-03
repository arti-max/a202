from dataclasses import dataclass
from enum import Enum, auto
import re

class TokenType(Enum):
    NUM = auto()        # Number (0 .. 15)
    BIN = auto()        # BinNum $(0 .. 1)
    REGISTER = auto()   # R0 .. R15
    INSTR = auto()      # Instruction
    LABEL = auto()      # Label (start:)
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: str = ""
    line: int = 0
    column: int = 0

INSTRUCTIONS = {
    'NOP', 'LDM', 'SWP', 'ADD', 'JUN', 'JC', 'OUT'
}

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
        if self.pos < len(self.source):
            self.current_char = self.source[self.pos]
        else:
            self.current_char = None

    def skip_whitespace_and_comments(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == ';':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                if self.current_char == '\n':
                    self.advance()
            else:
                break

    def read_bin(self):
        self.advance()  # Consume '$'
        if self.current_char is None:
            raise Exception(f"Unexpected end after $ at line {self.line}, column {self.column}")
        bin_digit_1 = self.current_char
        self.advance()
        bin_digit_2 = self.current_char
        if (bin_digit_1.upper() not in '01') or (bin_digit_2 not in '01'):
            raise Exception(f"Invalid bin digit '{bin_digit_1}{bin_digit_2}' at line {self.line}, column {self.column}")
        value = f"{bin_digit_1.upper()}{bin_digit_2.upper()}"
        self.advance()
        return value

    def read_number(self):
        digits = []
        while self.current_char is not None and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()
        return ''.join(digits)

    def read_register(self):
        reg_char = self.current_char
        self.advance()  # Consume 'R'
        digits = []
        while self.current_char is not None and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()
        if not digits:
            raise Exception(f"Missing register number at line {self.line}, column {self.column}")
        reg_num = ''.join(digits)
        if 0 <= int(reg_num) <= 15:
            return reg_char.upper() + reg_num
        else:
            raise Exception(f"Register {reg_num} out of range 0-15 at line {self.line}, column {self.column}")

    def read_identifier(self):
        identifier = []
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier.append(self.current_char)
            self.advance()
        return ''.join(identifier)

    def get_next_token(self):
        self.skip_whitespace_and_comments()

        if self.current_char is None:
            return Token(TokenType.EOF, line=self.line, column=self.column)

        start_line = self.line
        start_column = self.column

        # Check for BIN
        if self.current_char == '$':
            bin_value = self.read_bin()
            return Token(TokenType.BIN, bin_value, line=start_line, column=start_column)

        # Check for NUM
        if self.current_char.isdigit():
            num_str = self.read_number()
            num = int(num_str)
            if 0 <= num <= 15:
                return Token(TokenType.NUM, num_str, line=start_line, column=start_column)
            else:
                raise Exception(f"Number {num} out of range 0-15 at line {start_line}, column {start_column}")

        # Check for REGISTER (R followed by digits)
        if self.current_char.upper() == 'R':
            # Peek next character to see if it's a digit
            next_pos = self.pos + 1
            if next_pos < len(self.source) and self.source[next_pos].isdigit():
                reg = self.read_register()
                return Token(TokenType.REGISTER, reg, line=start_line, column=start_column)

        # Check for LABEL or INSTR
        if self.current_char.isalpha() or self.current_char == '_':
            identifier = self.read_identifier()
            # Check if it's a label
            if self.current_char == ':':
                self.advance()  # Consume ':'
                return Token(TokenType.LABEL, identifier, line=start_line, column=start_column)
            else:
                # Check if it's an instruction
                if identifier.upper() in INSTRUCTIONS:
                    return Token(TokenType.INSTR, identifier.upper(), line=start_line, column=start_column)
                else:
                    raise Exception(f"Unknown identifier '{identifier}' at line {start_line}, column {start_column}")

        # If none matched, raise error
        raise Exception(f"Unexpected character '{self.current_char}' at line {start_line}, column {start_column}")