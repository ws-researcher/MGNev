import heapq
from filecmp import cmp


class HeapNode:

    def __init__(self, id: str, value: float):
        self.id = id
        self.value = value

    def __lt__(self, other):
        return self.value < other.value


class MinHeap(object):

    def __init__(self):
        self._data = []
        self.idIndex = dict()

    def size(self):
        return len(self._data)

    def isEmpty(self):
        return len(self._data) == 0

    def push(self, heapNode: HeapNode):
        # 插入元素入堆

        self._data.append(heapNode)

        self.idIndex[heapNode.id] = len(self._data) - 1
        self._shiftup(len(self._data) - 1)


    def pop(self):
        # 出堆
        ret = None
        if len(self._data) == 0:
            return None
        elif len(self._data) == 1:
            ret = self._data[0]
            self._data = []
            self.idIndex = dict()
        elif len(self._data) >=2:
            ret = self._data[0]
            self._data[0] = self._data[-1]

            data = self._data[-1]
            self.idIndex[data.id] = 0

            self._data = self._data[0:-2]
            self.idIndex.pop(ret.id)

            self._shiftDown(0)

        return ret



    def _shiftup(self, index):
        # 上移self._data[index]，以使它不大于父节点
        parent = (index - 1) >> 1
        if 0 < parent < len(self._data):
            parentData = self._data[parent]
            indexData = self._data[index]
            while index > 0 and parentData.value > indexData.value:
                # swap
                self._data[parent], self._data[index] = self._data[index], self._data[parent]
                self.idIndex[indexData.id] = parent
                self.idIndex[parentData.id] = index
                index = parent
                parent = (index - 1) >> 1
                parentData = self._data[parent]
                indexData = self._data[index]


    def _shiftDown(self, index):
        # 上移self._data[index]，以使它不小于子节点
        j = (index << 1) + 1
        while 0 < j < len(self._data):
            jData = self._data[j]
            indexData = self._data[index]
            if j + 1 < len(self._data):
                j1Data = self._data[j + 1]
                if j1Data.value < jData.value:
                    j += 1
            # 有子节点
            if j + 1 < len(self._data) and j1Data.value < jData.value:
                # 有右子节点，并且右子节点较大
                j += 1
            jData = self._data[j]
            if indexData.value <= jData.value:
                # 堆的索引位置已经大于两个子节点，不需要交换了
                break
            self._data[index], self._data[j] = self._data[j], self._data[index]
            self.idIndex[indexData.id] = j
            self.idIndex[jData.id] = index
            index = j
            j = (index << 1) + 1

        return index


    def pushAndChange(self, heapNode: HeapNode):
        # 插入元素入堆
        id = heapNode.id
        if id not in self.idIndex.keys():
            self._data.append(heapNode)

            self.idIndex[heapNode.id] = len(self._data) - 1
            self._shiftup(-1)
        else:
            index = self.idIndex.get(id)
            node = self._data[index]
            if node.value > heapNode.value:
                self._shiftup(index)
            elif node.value < heapNode.value:
                self._shiftDown(index)
            else:
                pass


    def getTop(self):
        return self._data[0]

    def getAllTop(self):
        nodes = set()
        topNode = self.getTop()
        nodes.add(topNode)
        act = topNode.value
        for node in self._data:
            if node.value == act:
                nodes.add(node)

        return nodes

# class Skill(object):
#     def __init__(self, activation, id):
#         self.activation = activation
#         self.id = id
#
#     # 下面两个方法重写一个就可以了
#     def __lt__(self, other):  # operator <
#         return self.activation > other.priority
#
#     # def __cmp__(self, other):
#     #     # call global(builtin) function cmp for int
#     #     return cmp(self.activation, other.priority)
#
#     def __str__(self):
#         return '(' + str(self.activation) + ',\'' + self.id + '\')'
