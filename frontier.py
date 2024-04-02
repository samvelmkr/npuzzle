from collections import deque
import heapq

class Frontier:
    def __init__(self):
        self.max_nodes_stored = 0

    def add(self, node):
        pass

    def clear(self):
        pass

    def is_empty(self):
        pass

    def pop(self):
        pass

    def get_generated_nodes(self):
        return self.max_nodes_stored


class DepthFirstFrontier(Frontier):
    def __init__(self):
        super().__init__()
        self.stack = []

    def add(self, node):
        self.max_nodes_stored += 1
        self.stack.append(node)

    def clear(self):
        self.stack.clear()

    def is_empty(self):
        return len(self.stack) == 0

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    def get_generated_nodes(self):
        return self.stack


class BreadthFirstFrontier(Frontier):
    def __init__(self):
        super().__init__()
        self.queue = deque()

    def add(self, node):
        self.max_nodes_stored += 1
        self.queue.append(node)

    def clear(self):
        self.queue.clear()

    def is_empty(self):
        return len(self.queue) == 0

    def pop(self):
        if not self.is_empty():
            return self.queue.popleft()


class BestFirstFrontier(Frontier):
    def __init__(self, node_func):
        super().__init__()
        self.node_function = node_func
        self.list = []

    def add(self, node):
        node.value = self.node_function.produce(node)
        heapq.heappush(self.list, node)
        self.max_nodes_stored += 1

    def clear(self):
        self.list.clear()

    def is_empty(self):
        return len(self.list) == 0

    def pop(self):
        if not self.is_empty():
            return heapq.heappop(self.list)


