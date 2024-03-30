from collections import deque


class Frontier:
    def add(self, node):
        pass

    def clear(self):
        pass

    def is_empty(self):
        pass

    def remove(self):
        pass


class DepthFirstFrontier(Frontier):
    def __init__(self):
        self.stack = []

    def add(self, node):
        self.stack.append(node)

    def clear(self):
        self.stack.clear()

    def is_empty(self):
        return len(self.stack) == 0

    def remove(self):
        if not self.is_empty():
            return self.stack.pop()


class BreadthFirstFrontier(Frontier):
    def __init__(self):
        self.queue = deque()

    def add(self, node):
        self.queue.append(node)

    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return len(self.queue) == 0

    def remove(self):
        if not self.is_empty():
            return self.queue.popleft()
