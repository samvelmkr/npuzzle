import frontier

from collections import deque


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
            stepNo = 0
            while stack:
                node = stack.pop()
                print(stepNo, end = '')
                stepNo += 1
                if not node.parent:
                    print(': start')
                else:
                    print(': ', end = '')
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


class BreadthFirstTreeSearch:
    @staticmethod
    def find_solution(initial_state, goal_test):
        node = Node(None, None, initial_state)
        if goal_test.is_goal(node.state):
            return node
        fifo_frontier = frontier.BreadthFirstFrontier()
        fifo_frontier.add(node)
        while fifo_frontier:
            node = fifo_frontier.remove()
            for action in node.state.get_applicable_actions():
                new_state = node.state.get_action_result(action)
                child = Node(node, action, new_state)
                if goal_test.is_goal(new_state):
                    return child
                fifo_frontier.add(child)
        return None

