from ports import Port
from ram import RAM

class bit2_cpu:
    def __init__(self):
        self.regs = [0b00]*4
        self.acc = 0b00
        self.acbr = 0b00
        # Program Counter
        # Flags
        self.fs = [0, 0] # C, Z
        # instr regs
        self.ir = 0b0
        # 2 level stack
        self.sp = 0b0
        self.stack = [
        0b000000,
        # 2 levels
        0b000000,
        0b000000
        ]
        # other
        self.rom = None
        self.ports = []
        
        
    def set_flag(self, flag, data):
        self.fs[flag] = (data & 0b1)
        
    def set_reg(self, reg, data):
         self.regs[reg] = (data & 0b11)
     
    def set_acc(self, data):
        self.acc = (data & 0b11)
        self.set_flag(1, self.acc == 0)
        
    def get_pc(self):
        return self.stack[self.sp]
        
    def get_pch(self):
        """Верхние 2 бита PC (биты 5-4)"""
        return (self.get_pc() >> 4) & 0b11

    def get_pcm(self):
        """Средние 2 бита PC (биты 3-2)"""
        return (self.get_pc() >> 2) & 0b11

    def get_pcl(self):
        """Нижние 2 бита PC (биты 1-0)"""
        return self.get_pc() & 0b11

    def set_pc(self, pch=None, pcm=None, pcl=None):
        """Обновляет части PC"""
        current_pc = self.get_pc()
        new_pch = pch if pch is not None else self.get_pch()
        new_pcm = pcm if pcm is not None else self.get_pcm()
        new_pcl = pcl if pcl is not None else self.get_pcl()
        self.stack[self.sp] = (new_pch << 4) | (new_pcm << 2) | new_pcl
    
    def inc_pc(self):
        inc_data = ((self.get_pc()+1) & 0b111111)
        self.stack[self.sp] = inc_data
        
    def out_to_ports(self, index, data):
        for port in self.ports:
            port.set_data(index, data)
            
    def next_instr(self):
        self.ir = self.rom[self.get_pc()]
        self.inc_pc()
    
    def execute(self):
         print(bin(self.ir))
         if self.ir == 0b00: # nop
                pass
         elif self.ir == 0b01: # ldm dd
                self.next_instr()
                self.set_acc(self.ir)
         elif self.ir == 0b10: # swp rr
                self.next_instr()
                self.acbr = self.acc
                self.acc = self.regs[self.ir]
                self.regs[self.ir] = self.acbr
         elif self.ir == 0b11: # Extended (6bit)
                    self.next_instr()
                    print(f"Ex: {bin(self.ir)}")
                    if self.ir == 0b00: # add rr
                        self.next_instr()
                        data = self.acc + self.regs[self.ir] + self.fs[0]
                        carry = 1 if data > 0b11 else 0
                        self.set_flag(0, carry)
                        self.set_acc(data)
                    elif self.ir == 0b01: # jun rp
                         self.next_instr()
                         reg_pair = self.ir & 0b1
                         if reg_pair == 0b0:
                             pcm = self.regs[0]
                             pcl = self.regs[1]
                         else:
                              pcm = self.regs[2]
                              pcl = self.regs[3]
                          
                         self.set_pc(pcm=pcm, pcl=pcl)
                    elif self.ir == 0b10: # jc rp
                         self.next_instr()
                         reg_pair = self.ir & 0b1
                         if reg_pair == 0b0:
                             pcm = self.regs[0]
                             pcl = self.regs[1]
                         else:
                              pcm = self.regs[2]
                              pcl = self.regs[3]
                          
                         if self.fs[0] == 1:
                             self.set_pc(pcm=pcm, pcl=pcl)
                    elif self.ir == 0b11: # out dd
                          self.next_instr()
                          self.out_to_ports(self.ir, self.acc)
                          
                               
    def run(self):
        while self.get_pc() < len(self.rom):
            self.next_instr()
            self.execute()
        
        
        
cp = bit2_cpu()

p0 = Port(0b00)
p1 = Port(0b01)

ram = RAM()
p1.connected = ram

cp.ports.append(p0)
cp.ports.append(p1)

cp.rom = [ # assembly test
0b1, 0b11, 0b11, 0b11, 0b0, 0b1, 0b1, 0b10, 0b0

]

cp.run()

print("Acc: ",cp.acc)
print("Regs: ",cp.regs)
print("Flags: ",cp.fs)
print("PC: ",bin(cp.stack[0]))
print("======")
p0.print_data()
print("======")
p1.print_data()
print("======")
print(f"RAM: {ram.memory}")
print(f"RAM-mp: {ram.mp}")
print(f"RAM-buff: {ram.buffer}")
print(f"RAM-mode: {ram.mode}")