from __future__ import annotations
from frontier import *


class State:
    def get_applicable_actions(self):
        pass

    def get_action_result(self, action):
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass


class Action:
    def cost(self) -> int:
        return 1


class GoalTest:
    def is_goal(self, state):
        pass


class Node:
    def __init__(self, parent, action, state, depth=0):
        self.parent = parent
        self.action = action
        self.state = state
        self.depth = depth
        self.value = 0

        #  g(n)
        self.cost = self.calculate_cost()

    def calculate_cost(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.cost + self.action.cost()

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


class Printing:
    @classmethod
    def print_solution(cls, solution):
        if not solution:
            print('No solution found!')
        else:
            stack = deque()
            node = solution
            while node:
                stack.append(node)
                node = node.parent
            step_no = 0
            while stack:
                node = stack.pop()
                print(step_no, end='')
                step_no += 1
                if not node.parent:
                    print(': start')
                else:
                    print(': ', end='')
                    cls.print_action(node.action)
                    print()
                print()
                cls.print_state(node.state)
                print()

    @staticmethod
    def print_action(action):
        pass

    @staticmethod
    def print_state(state):
        pass


class NodeFunction:
    def produce(self, node):
        pass


# f(n)
class EvaluationFunction(NodeFunction):
    pass


# h1(n) - number of misplaced tiles
class HeuristicFunction1(NodeFunction):
    def produce(self, node) -> int:
            state = node.state
            res = 0

            goal_state_tile_value = 1
            for row in range(state.width):
                for col in range(state.width):
                    if state.get_tile(row, col) != 0 and \
                            state.get_tile(row, col) != goal_state_tile_value:
                        res += 1
                    goal_state_tile_value += 1

            return res


# h2(n) - total Manhattan distance
# (i.e. no. of squares from desired location of each tile)
class HeuristicFunction2(NodeFunction):
    @staticmethod
    def find_tile_right_pos(value, width):
        goal_state_tile_value = 1

        for row in range(width):
            for col in range(width):
                if value == goal_state_tile_value:
                    return row, col
                goal_state_tile_value += 1


    def produce(self, node) -> int:
        state = node.state
        res = 0

        for row in range(state.width):
            for col in range(state.width):
                value = state.get_tile(row, col)
                if value != 0:
                    goal_position = self.find_tile_right_pos(value, state.width)
                    res += abs(row - goal_position[0]) + abs(col - goal_position[1])

        return res


class AStarFunction(NodeFunction):
    def __init__(self, heuristic_function):
        self.heuristic = heuristic_function

    def produce(self, node) -> int:
        return node.cost + self.heuristic.produce(node)


class UCSFunction(NodeFunction):
    def produce(self, node) -> int:
        return node.cost


class Search:
    def __init__(self, frontier_behavior: Frontier) -> None:
        self.frontier: Frontier = frontier_behavior

    def find_solution(self, initial_state, goal_test):
        pass

    @staticmethod
    def get_last_search_gen_nodes(frontier: Frontier):
        return frontier.get_generated_nodes()


class IterativeDeepeningTreeSearch(Search):
    def __init__(self):
        super().__init__(frontier_behavior=DepthFirstFrontier())

    def find_solution(self, initial_state, goal_test):
        depth = 1
        while True:
            result = self.depth_limited_search(initial_state, goal_test, depth)

            if result != 'cutoff':
                return result

            # depth += 1
            depth *= 2

    def depth_limited_search(self,initial_state, goal_test, l):
        node = Node(None, None, initial_state, 1)
        self.frontier.add(node)
        result = None

        while not self.frontier.is_empty():
            node = self.frontier.pop()
            if goal_test.is_goal(node.state):
                return node

            if node.depth > l:
                result = 'cutoff'
                continue

            for action in node.state.get_applicable_actions():
                new_state = node.state.get_action_result(action)
                child = Node(node, action, new_state, node.depth + 1)
                if goal_test.is_goal(new_state):
                    return child
                self.frontier.add(child)

        return result


class TreeSearch(Search):
    def __init__(self, frontier_behavior: Frontier) -> None:
        super().__init__(frontier_behavior)

    def find_solution(self, initial_state, goal_test):
        total_nodes_generated = 1
        self.frontier.reset_nodes_count()
        node = Node(None, None, initial_state)
        if goal_test.is_goal(node.state):
            # print("Total nodes generated:", total_nodes_generated)
            # print("Max nodes on frontier:", self.frontier.get_generated_nodes())
            return node
        self.frontier.add(node)

        while not self.frontier.is_empty():
            node = self.frontier.pop()
            for action in node.state.get_applicable_actions():
                new_state = node.state.get_action_result(action)
                child = Node(node, action, new_state)
                total_nodes_generated += 1

                if goal_test.is_goal(new_state):
                    # print("Total nodes generated:", total_nodes_generated)
                    # print("Max nodes on frontier:",  self.frontier.get_generated_nodes())
                    return child

                self.frontier.add(child)

        # print("Total nodes generated:", total_nodes_generated)
        # print("Max nodes on frontier:", self.frontier.get_generated_nodes())
        return None


class BreadthFirstTreeSearch(TreeSearch):
    def __init__(self):
        super().__init__(frontier_behavior=BreadthFirstFrontier())


class DepthFirstTreeSearch(TreeSearch):
    def __init__(self):
        super().__init__(frontier_behavior=DepthFirstFrontier())


class GreedyBestFirstTreeSearch(TreeSearch):
    def __init__(self, heuristic_function):
        super().__init__(frontier_behavior=BestFirstFrontier(heuristic_function))


class UCSTreeSearch(TreeSearch):
    def __init__(self):
        super().__init__(frontier_behavior=BestFirstFrontier(UCSFunction()))


class AStarTreeSearch(TreeSearch):
    def __init__(self, heuristic_function):
        super().__init__(frontier_behavior=BestFirstFrontier(AStarFunction(heuristic_function)))



class GraphSearch(Search):
    def __init__(self, frontier_behavior: Frontier) -> None:
        super().__init__(frontier_behavior)

    def find_solution(self, initial_state, goal_test):
        total_nodes_generated = 1
        self.frontier.reset_nodes_count()
        node = Node(None, None, initial_state)
        if goal_test.is_goal(node.state):
            # print("Total nodes generated:", total_nodes_generated)
            # print("Max nodes on frontier:", self.frontier.get_generated_nodes())
            return node

        self.frontier.add(node)
        expanded = set()

        while not self.frontier.is_empty():
            node = self.frontier.pop()
            if node.state not in expanded:
                if goal_test.is_goal(node.state):
                    # print("Total nodes generated:", total_nodes_generated)
                    # print("Max nodes on frontier:", self.frontier.get_generated_nodes())
                    return node
                expanded.add(node.state)
                for action in node.state.get_applicable_actions():
                    new_state = node.state.get_action_result(action)
                    if new_state not in expanded:
                        child = Node(node, action, new_state)
                        total_nodes_generated += 1

                        self.frontier.add(child)

        # print("Total nodes generated:", total_nodes_generated)
        # print("Max nodes on frontier:", self.frontier.get_generated_nodes())
        return None


class BreadthFirstGraphSearch(GraphSearch):
    def __init__(self):
        super().__init__(frontier_behavior=BreadthFirstFrontier())


class DepthFirstGraphSearch(GraphSearch):
    def __init__(self):
        super().__init__(frontier_behavior=DepthFirstFrontier())


class GreedyBestFirstGraphSearch(GraphSearch):
    def __init__(self, heuristic_function):
        super().__init__(frontier_behavior=BestFirstFrontier(heuristic_function))


class AStarGraphSearch(GraphSearch):
    def __init__(self, heuristic_function):
        super().__init__(frontier_behavior=BestFirstFrontier(AStarFunction(heuristic_function)))


class UCSGraphSearch(GraphSearch):
    def __init__(self):
        super().__init__(frontier_behavior=BestFirstFrontier(UCSFunction()))
