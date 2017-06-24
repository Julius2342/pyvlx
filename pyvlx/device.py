
class Device:
    def __init__(self, pyvlx, id, name):
        self.pyvlx = pyvlx
        self.id = id
        self.name = name

    def get_name(self):
        return self.name
