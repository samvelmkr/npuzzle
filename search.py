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
    pass


class GoalTest:
    def is_goal(self, state):
        pass


class Node:
    def __init__(self, parent, action, state):
        self.parent = parent
        self.action = action
        self.state = state


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


class Search:
    def __init__(self, frontier_behavior: type[Frontier]) -> None:
        self.FrontierType: type[Frontier] = frontier_behavior

    def find_solution(self, initial_state, goal_test):
        pass

    @staticmethod
    def get_last_search_gen_nodes(frontier: Frontier):
        return frontier.get_generated_nodes()


class TreeSearch(Search):
    def __init__(self, frontier_behavior: type[Frontier]) -> None:
        super().__init__(frontier_behavior)

    def find_solution(self, initial_state, goal_test):
        node = Node(None, None, initial_state)
        if goal_test.is_goal(node.state):
            return node
        frontier = self.FrontierType()
        frontier.add(node)

        while not frontier.is_empty():
            node = frontier.pop()
            for action in node.state.get_applicable_actions():
                new_state = node.state.get_action_result(action)
                child = Node(node, action, new_state)
                if goal_test.is_goal(new_state):
                    return child
                frontier.add(child)
        return None


class BreadthFirstTreeSearch(TreeSearch):
    def __init__(self):
        super().__init__(
            frontier_behavior=BreadthFirstFrontier
        )


class GraphSearch(Search):
    def __init__(self, frontier_behavior: type[Frontier]) -> None:
        super().__init__(frontier_behavior)

    def find_solution(self, initial_state, goal_test):
        node = Node(None, None, initial_state)
        if goal_test.is_goal(node.state):
            return node
        frontier = self.FrontierType()
        frontier.add(node)
        expanded = set()

        while not frontier.is_empty():
            node = frontier.pop()
            if node.state not in expanded:
                if goal_test.is_goal(node.state):
                    return node
                expanded.add(node.state)
                for action in node.state.get_applicable_actions():
                    new_state = node.state.get_action_result(action)
                    if new_state not in expanded:
                        child = Node(node, action, new_state)
                        frontier.add(child)
        return None


class BreadthFirstGraphSearch(GraphSearch):
    def __init__(self):
        super().__init__(
            frontier_behavior=BreadthFirstFrontier
        )
