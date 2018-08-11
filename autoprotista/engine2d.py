#!/bin/python

from .engine import Engine

import numpy as np
import itertools
import yaml
import random


class Engine2d(Engine):
    def __init__(self, rule_file):
        self.Dimensions = 2

        if 'random' in rule_file:
            rules = self.randomizeRule()
            yaml.dump(rules, open('rules/random.yaml', 'w'))
        else:
            rules = yaml.load(open(rule_file))

        print(rules)
        self.activateCell = rules['activate']
        self.deactivateCell = rules['deactivate']

        self.neighborhoodType = rules['neighborhoodType']
        try:
            self.initialMethod = rules['initial']['method']
            self.initialMethodPosition = rules['initial']['position']
            self.initialSize = rules['initial']['size']
        except Exception as e:
            print("Failure to read initial state of rule.\nFalling back to standard...")
            self.initialMethodPosition = 'central'
            self.initialMethod = 'bar'
            self.initialSize = 1

        Engine.__init__(self)

    def randomizeRule(self):
        activate = {}

        def getAllPrevious(activate):
            a = [activate[k] for k in activate.keys()]
            a = [x for x in a for x in a]
            return a
        for k in range(1, 7):
            if random.random() < 1 / k - 0.1:
                entry_activate = []
                for n in range(1, 7):
                    if random.random() < 1 / n - 0.1:
                        if n not in getAllPrevious(activate):
                            entry_activate.append(n)
                activate[k] = entry_activate[:]

        deactivate = [random.randrange(1, 9) for i in range(random.randrange(1, 5))]

        rules = {
            'activate': activate,
            'deactivate': deactivate,
            'neighborhoodType': random.randrange(0, 2),
            'initial': {
                'method': random.choice(['bar', 'plus']),
                'position': random.choice(['central', 'quarter']),
                'size': random.randrange(1, 3)
            }

        }
        return rules

    @staticmethod
    def neumannNeighborhood(state, x, y):
        neighborhood = [
            state[x-1][y],
            state[x][y-1],
            state[x][y],
            state[x][y+1],
            state[x+1][y]
        ]
        return neighborhood

    @staticmethod
    def mooreNeighborhood(state, y, x):
        neighborhood = [
            state[y-1][x-1],
            state[y][x-1],
            state[y+1][x-1],
            state[y-1][x],
            state[y][x],
            state[y+1][x],
            state[y-1][x+1],
            state[y][x+1],
            state[y+1][x+1]
        ]
        return neighborhood

    def step(self, state=None):

        last_state = state if state else self.retrieve(-1)

        current_state = np.zeros(self.Shape)
        neighborhoodMethod = {
            0: self.neumannNeighborhood,
            1: self.mooreNeighborhood
        }[self.neighborhoodType]

        activateCellValues = self.activateCell.keys()
        for r, row in enumerate(last_state):
            if r == 0 or r == len(last_state) - 1:
                continue
            for c, col in enumerate(row):
                if c == 0 or c == len(row) - 1:
                    continue

                neighborhood = neighborhoodMethod(last_state, r, c)

                # neighborhood = sum(neighborhood) / len(neighborhood)
                neighborhoodScore = sum(neighborhood)
                if not last_state[r, c]:
                    for W in activateCellValues:
                        if neighborhoodScore in self.activateCell[W]:
                            current_state[r, c] = W
                            break

                elif last_state[r, c] and neighborhoodScore - 1 in self.deactivateCell:
                    current_state[r, c] = 0
                else:
                    current_state[r, c] = last_state[r, c]

                # current_state[r, c] = new_value

        #print(sum(current_state))
        #print(current_state.shape)
        return current_state

    def setup(self):
        self.Shape = (self.Size, self.Size)

        initialState = np.zeros(self.Shape)
        startingRow = self.initialSize

        def generatePoints(x, y, size, verticalArm=False, horizontalArm=True):
            a = [[x, y]]
            for k in range(1, size//2):
                if horizontalArm:
                    a.append([x, y - k])
                    a.append([x, y + k])
                if verticalArm:
                    a.append([x - k, y])
                    a.append([x + k, y])
            return a

        if 'bar' in self.initialMethod:
            verticalArm = False
            horizontalArm = True
        elif 'plus' in self.initialMethod:
            verticalArm = True
            horizontalArm = True

        else:
            exit("Invalid initial shape method: %s." % self.initialMethodPosition)

        if 'central' in self.initialMethodPosition:
            mid = self.Size//2
            matrix = generatePoints(mid, mid,
                                    self.initialSize, verticalArm, horizontalArm)

        elif 'quarter' in self.initialMethodPosition:
            quarter = self.Size//4
            prematrix = itertools.product([1, 3], repeat=2)

            matrix = []
            for node in prematrix:
                matrix += generatePoints(node[0] * quarter,
                                         node[1] * quarter,
                                         self.initialSize,
                                         verticalArm,
                                         horizontalArm)
        else:
             exit("Invalid initial position method: %s." % self.initialMethod)

        for node in matrix:
            initialState[node[0], node[1]] = 1

        return initialState
