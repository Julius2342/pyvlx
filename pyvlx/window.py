from .device import Device

class Window(Device):

    def __init__(self, pyvlx, id, name, subtype, typeId):
        self.pyvlx = pyvlx
        self.id = id
        self.name = name
        self.subtype = subtype
        self.typeId = typeId
        Device.__init__(self, pyvlx, id, name)


    @classmethod
    def from_config(cls, pyvlx, item):
        name = item['name']
        id = item['id']
        subtype = item['subtype']
        typeId = item['typeId']
        return cls(pyvlx, id, name, subtype, typeId)


    def __str__(self):
        return '<Window name="{0}" ' \
				    'id="{1}" ' \
                    'subtype="{2}" ' \
                    'typeId="{3}" />' \
                    .format(
                        self.name,
                        self.id,
                        self.subtype,
                        self.typeId)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



