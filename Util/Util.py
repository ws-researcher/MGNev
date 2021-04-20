class Stack(object):

    def __init__(self):
        self.__list = []

    def __len__(self):
        return len(self.__list)

    def __iter__(self):
        return iter(self.__list)

    def __str__(self):
        return str(self.__list)

    def is_empty(self):
        return self.__list == []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        if self.is_empty():
            return
        else:
            return self.__list.pop()

    def top(self):
        if self.is_empty():
            return
        else:
            return self.__list[-1]

    def toList(self):
        return self.__list

    def toSet(self):
        return set(self.__list)

    def __getitem__(self, index):
        if self.is_empty():
            return
        else:
            return self.__list[index]

    def index(self, item):
        return self.__list.index(item)