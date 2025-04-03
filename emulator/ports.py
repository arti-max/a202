

class Port:
    def __init__(self, _indx):
        self.data = 0b00
        self.index = _indx
        self.connected = None
    
    def set_data(self, indx, data):
        if indx == self.index:
            self.data = data & 0b11
            self.transfer_data()
    
    def transfer_data(self):
            if self.connected:
                self.connected.get_input(self.data)
            
    def print_data(self):
        print(f"Port index: {bin(self.index)}")
        print(f"Port data: {bin(self.data)}")