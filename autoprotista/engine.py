#!/bin/python


class Engine(object):

    def __init__(self):

        self.Size = 120
        self.Width = 120

        self.states = [self.setup()]

    def retrieve(self, number):
        return self.states[number]

    def currentState(self):
        return self.retrieve(len(self.states) - 1)

    def run_one_iteration(self, handler=None, width=None):
        row = self.step()

        if handler is not None:
            handler(row, width)
        self.states.append(row)

        row_sums = row.max()
        new_matrix = row / row_sums
        return new_matrix

    def run(self, handler=None, width=None, iterations=None):
        nb_iterate = iterations if iterations else int(10e11)
        for i in range(nb_iterate):
            self.run_one_iteration(handler, width)
