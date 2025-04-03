

class RAM:
    def __init__(self):
        self.memory = [0b00]*32
        self.mp = 0b000000
        self.buffer = 0b00
        self.mode = 0b00
        
    def get_mph(self):
        """Верхние 2 бита MP (биты 5-4)"""
        return (self.mp >> 4) & 0b11

    def get_mpm(self):
        """Средние 2 бита MP (биты 3-2)"""
        return (self.mp >> 2) & 0b11

    def get_mpl(self):
        """Нижние 2 бита MP (биты 1-0)"""
        return self.mp & 0b11
        
    def set_mp(self, mph=None, mpm=None, mpl=None):
        """Обновляет части PC"""
        current_mp = self.mp
        new_mph = mph if mph is not None else self.get_mph()
        new_mpm = mpm if mpm is not None else self.get_mpm()
        new_mpl = mpl if mpl is not None else self.get_mpl()
        self.mp = (new_mph << 4) | (new_mpm << 2) | new_mpl
        
    def get_input(self, data):
        if self.buffer == 0b00: # 1 step
            self.mode = (data & 0b11)
            self.buffer = (self.buffer + 1) & 0b11
        elif self.buffer == 0b01:
            if self.mode == 0b00:
                self.set_mp(mpl=data)
            elif self.mode == 0b01:
                self.set_mp(mpm=data)
            elif self.mode == 0b10:
                self.set_mp(mph=data)
            self.buffer = (self.buffer + 1) & 0b11
        elif self.buffer == 0b10:
             if self.mode == 0b00:
                 self.memory[self.mp] = data & 0b11
             self.buffer = 0b00