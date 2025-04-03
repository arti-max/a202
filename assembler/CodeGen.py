

class CodeGenContext:
    OPCODE_MAP = {
        "NOP"   : 0b00,
        "LDM"   : 0b01,
        "SWP"   : 0b10,
    }
    EXT_OPCODE_MAP = {
        "ADD"   : 0b00,
        "JUN"   : 0b01,
        "JC"    : 0b10,
        "OUT"   : 0b11
    }
    
    REG_MAP = {
        "R0"    : 0x0,
        "R1"    : 0x1,
        "R2"    : 0x2,
        "R3"    : 0x3,
    }
    
    
    def __init__(self, file):
        self.out_file = file
        self.BIN_CODE = []
    
    def add_bin(self, first_num, second_num):
        # Обрезаем числа до 4 бит и объединяем в байт
        # Форматируем результат в виде 0xAB с заглавными буквами
        self.BIN_CODE.append(str(bin(first_num & 0b11)))
        self.BIN_CODE.append(str(bin(second_num & 0b11)))
    
    def add_bin_6(self, higher_num, middle_num, low_num):
        # Обрезаем числа до 4 бит и объединяем в байт
        # Форматируем результат в виде 0xAB с заглавными буквами
        self.BIN_CODE.append(str(bin(higher_num & 0b11)))
        self.BIN_CODE.append(str(bin(middle_num & 0b11)))
        self.BIN_CODE.append(str(bin(low_num & 0b11)))
        
        
    def generate(self) -> bin:
        print("\n[DEBUG] Generating BIN CODE...")
        with open(self.out_file, "w") as f:
            f.write(", ".join(self.BIN_CODE))
            
        return self.BIN_CODE