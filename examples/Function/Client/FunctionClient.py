from clusterer import ProtocolClient

if __name__ == '__main__':
    p = ProtocolClient(50000,b'password')
    p.run()