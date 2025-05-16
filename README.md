# QSim
QSim is a minimal implementation of a quantum computer in NumPy Python.

This side project is mostly just for me to play around with quantum information. Many useful features are missing!

## Structure
The package is divided into two files:
* **`system`:** Implements the `System` class, to which you can apply quantum logic gates, measure the state of, and (unphysically) inspect the state of.
* **`gates`:** Utility functions for creating quantum logic gates.

Features that would be useful to implement to future:
1. Ability to measure some gates but not others.
2. Easier interface for creating quantum gates (e.g. ability to create gates from tensor products of gates with different sizes).

## Examples
1. Bell state
2. Deutsch--Jozsa algorithm
3. Grover's algorithm
4. More coming!