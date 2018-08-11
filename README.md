# Autoprotista

A python module all about cellular automata, one dimensional and two dimensional.<br>
It displays simulations through matplotlib animations.

## Installation

`sudo pip setup.py install`

## Usage

    ./run.py -d 2 -r random

Thats an starting point. It also supports 1d (`-d 1`) automata, for which we use a rule number like the famous 30 (`-r 30`).
Rules for 2d automata are stored in `rules`, so we call them like `-r rule`. 

## Save

Last randomized rule for 2D automata (as called in our example) is written as `random.yml`, so just rename it if it turns out to be cool xD. Of course you can create 
your own rule on that directory.

## 1D Rules

1D rules are described at [Elementary Cellular Automaton](http://mathworld.wolfram.com/ElementaryCellularAutomaton.html).

## 2D Rules

Those `.yaml` files that hold 2D rules have parameters that are mostly self explanatory.

