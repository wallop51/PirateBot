class List2D:
    def __init__(self, x_length: int, y_length: int, default=None, values: list=None):
        if values == None:
            self.values = [default for i in range(x_length * y_length)]
        else:
            self.values = list(values)

        self.x_length, self.y_length = x_length, y_length
        self.get_index = lambda x, y : y * x_length + x

    def __getitem__(self, x, y) -> tuple:
        return tuple(self.values[self.get_index(x, y)])
    
    def __setitem__(self, loc, value):
        x, y = loc
        self.values[self.get_index(x, y)] = value
        return None

    def __iter__(self):
        self.i = 0
        return self
    def __next__(self) -> tuple:
        sublist = tuple(self.values[self.i*self.x_length: (self.i + 1)*self.x_length])
        self.i += 1
        if self.i > self.y_length: raise StopIteration
        return sublist