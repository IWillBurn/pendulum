import time


class Closer:
    def __init__(self, root, treads):
        self.is_closed = False
        self.root = root
        self.treads = treads

    def close(self):
        print('Waiting for closing treads...')
        self.is_closed = True
        for tread in self.treads:
            tread.join()
        self.root.destroy()
        print('Closed')
