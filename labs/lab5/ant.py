
class Ant:
    def __init__(self, path):
        self.__path = path
        self.__length = 10000000

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        self.__path = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    def is_fitter_than(self, other_ant):
        return self.__length < other_ant.length

    def __str__(self):
        return "length " + str(self.__length) + ", path: " + str(self.__path)
