import yaml

class Config:

    def __init__(self, path=None, host=None, password=None):
        if path is not None:
            self.read_config(path)
        if host is not None:
            self.host = host
        if password is not None:
            self.password = password


    def read_config(self, path):
        print('Reading {0}'.format(path))
        with open(path, 'r') as filehandle:
            doc = yaml.load(filehandle)
            if not 'config' in doc:
                raise Exception('no element config found in: {0}'.format(path))
            if not 'host' in doc['config']:
                raise Exception('no element host found in: {0}'.format(path))
            if not 'password' in doc['config']:
                raise Exception('no element password found in: {0}'.format(path))
            self.host = doc['config']['host']
            self.password = doc['config']['password']
