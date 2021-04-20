import heapq
from filecmp import cmp


class HeapNode:

    def __init__(self, id: str, activation: float):
        self.id = id
        self.activation = activation


class MaxHeap(object):

    def __init__(self):
        self._data = []
        self._count = len(self._data)
        self.idIndex = dict()

    def size(self):
        return self._count

    def isEmpty(self):
        return self._count == 0

    def push(self, heapNode: HeapNode):
        # 插入元素入堆

        if self._count >= len(self._data):
            self._data.append(heapNode)
        else:
            self._data[self._count] = heapNode

        self.idIndex[heapNode.id] = self._count
        self._count += 1
        self._shiftup(self._count - 1)


    def pop(self):
        # 出堆
        if self._count > 0:
            ret = self._data[0]
            self._data[0] = self._data[self._count - 1]
            data = self._data[self._count - 1]
            self.idIndex[data.id] = 0
            self._count -= 1
            self._shiftDown(0)
            return ret

    def _shiftup(self, index):
        # 上移self._data[index]，以使它不大于父节点
        parent = (index - 1) >> 1
        parentData = self._data[parent]
        indexData = self._data[index]
        while index > 0 and parentData.activation < indexData.activation:
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
        while j < self._count:
            jData = self._data[j]
            indexData = self._data[index]
            j1Data = self._data[j + 1]
            # 有子节点
            if j + 1 < self._count and j1Data.activation > jData.activation:
                # 有右子节点，并且右子节点较大
                j += 1
            jData = self._data[j]
            if indexData.activation >= jData.activation:
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
            if self._count >= len(self._data):
                self._data.append(heapNode)
            else:
                self._data[self._count] = heapNode

            self.idIndex[heapNode.id] = self._count
            self._count += 1
            self._shiftup(self._count - 1)
        else:
            index = self.idIndex.get(id)
            node = self._data[index]
            if node.activation < heapNode.activation:
                self._shiftup(index)
            elif node.activation > heapNode.activation:
                self._shiftDown(index)
            else:
                pass


    def getTop(self):
        return self._data[0]

    def getAllTop(self):
        nodes = set()
        topNode = self.getTop()
        nodes.add(topNode)
        act = topNode.activation
        for node in self._data:
            if node.activation == act:
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
