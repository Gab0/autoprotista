#!/usr/bin/env python
import os

from optparse import OptionParser

import autoprotista
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import cm

DEFAULT_RULE = 30

rule_list = os.listdir('rules')
parser = OptionParser(
    usage="%%prog [options]\n\nElementary Cellular Automata.\nAvailable rules:\n%s" % '\n'.join(rule_list)
)

parser.add_option(
    "-r",
    "--rulename",
    dest="ruleName",
    default="",
    help="Which elementary cellular automaton rule to run."
)

parser.add_option(
    "-d",
    "--dimensions",
    dest="dimensions",
    default=1,
    type='int',
    help="Number of dimensions on the simulation.")

parser.add_option(
    "-s",
    "--steps",
    dest="maxSteps",
    default=700,
    help="Number of steps to simulate.")


def run(automaton):
    rest = automaton.currentState()

    figure, ax = plt.subplots()
    mat = ax.matshow(rest, cmap=cm.ocean)

    def update(d):
        state = automaton.run_one_iteration()
        mat.set_data(state)
        return state

    animator = animation.FuncAnimation(figure, update,
                                       interval=20, frames=options.maxSteps)
    plt.show()


if __name__ == "__main__":
    (options, arguments) = parser.parse_args(sys.argv[1:])

    if options.dimensions == 1:
        rule_number = int(options.ruleName) if options.ruleName else DEFAULT_RULE
        automatonEngine = autoprotista.Engine1d(rule_number)
    elif options.dimensions == 2:
        rule_name = options.ruleName if options.ruleName else 'rule'
        ruleSuffix = '.yaml'
        if not rule_name.endswith(ruleSuffix):
            rule_name += ruleSuffix
        rule_file = os.path.join('rules', rule_name)
        automatonEngine = autoprotista.Engine2d(rule_file)
    else:
        exit("Unsupported dimensional count: %i." % options.dimensions)

    run(automatonEngine)
