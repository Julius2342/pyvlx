
class Device:
    def __init__(self, pyvlx, ident, name):
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name

    def get_name(self):
        return self.name
