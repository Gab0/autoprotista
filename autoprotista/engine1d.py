#!/bin/python
import numpy as np
import copy

from .engine import Engine


class Engine1d(Engine):
    def __init__(self, rule_number):
        self.rule_number = rule_number
        self.rules = [self.integerToByte(v) for v in range(7, -1, -1)]
        self.rule = self.get_rule(rule_number)

        Engine.__init__(self)
        self.Dimensions = 1
    @staticmethod
    def integerToByte(value):
        a = '{0:03b}'.format(value)
        v = []
        for n in a:
            val = True if int(n) else False
            v.append(val)
        return v

    def get_rule(self, number):
        A = list('{0:08b}'.format(number))
        rules_to_apply = [bool(int(i)) for i in A]
        print(A)
        print(rules_to_apply)
        rules = []
        for i, rule in enumerate(rules_to_apply):
            if rule:
                rules.append(self.rules[i])
        return rules

    def setup(self):
        randomInit = False
        self.Shape = (self.Size, self.Width)
        initialState = np.zeros(self.Shape)
        if randomInit:
            pass
        else:
            mid = self.Width//2
            initialState[0, mid] = 1

        return initialState

    def step(self, state=None):
        next_row = []
        last_state = state if state else self.retrieve(-1)
        current_state = copy.deepcopy(last_state)
        current_index = len(self.states)
        last_index = current_index - 1

        for index, value in enumerate(last_state[current_index]):
            # skip first and last values (because of the padding)
            if index == 0 or index == len(last_state) - 1:
                continue

            # Upward state is the three cells above this one.
            upward_state = last_state[last_index, index - 1: index + 2]
            match = 1 if list(upward_state) in self.rule else 0
            current_state[current_index, index] = match

        return current_state

