class NodeError(RuntimeError):
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return str(self.arg)