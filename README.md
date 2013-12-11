WPM1PY
======
Python implementation of wpm1 algorithm. 

This version attempts to be an educational version of the algorithm, 
aspects such as performance were not taken into account.

## WPM1 ##

Is a SAT-Based Weighted MaxSAT solver algorithm created by, Carlos Ansótegui,
Maria Luisa Bonet, Joel Gabàs and Jordi Levy.

A detailed explanation of the algorithm can be found [here][paper].

## Implementation details ##

The implementation of the algorithm relies on an external SAT-solver which is called
by using the [satsolver.SATSolver][SATSolver] interface. This means that creating
a new class inheriting from satsolver.SATSolver and overriding the necessary methods,
we can test the algorithm with different SAT-solvers.

The [provided][picosat_ex] basic implementation uses the [PicoSAT][picosat_home] solver
as an external executable file (only provided for linux x86 and x64 and Mac OS X 64bits)
and uses files to send and retrieve data. But the implementation should be possible using
a wrapper to call the solver's API directly.

There are two restrictions for the solver interface implementations:
  1. All the methods on the base class have to be overrided.
  2. The \__init\__ method can't expect arguments.

## Using WPM1PY ##

To run the solver has to be executed the wpm1py.py file using at least Python 2.6.

#### Parameters ####

The solver accepts two parameters:

  + infile [optional]
    + This parameter is positional, it is specified without any flag and has to be a 
      file with the SAT, partial weighted MaxSAT or weighted MaxSAT formula that the 
      solver has to solve. If it is left unspecified stdin is assumed by default.

  + solver [optional]
    + This parameter is specified using the flag -s/--solver and lets change the SAT-solver
      used by the WPM1 algorithm. The expected value looks like a python import path 
      _(package.module.class)_ and must specify a python class that inherits 
      from satsolver.SATSolver. By default picosat.PicoSAT is used.

      + Example:
      
        If we want to use our solver implementation SuperSolver, which is defined in the 
        python module spsolver.py. The _solver_ parameter will be (assuming that is in
        the same folder than the wpm1py.py):
        
        -s _spsolver.SuperSolver_





[paper]: http://www.iiia.csic.es/~levy/papers/CP12.pdf
[SATSolver]: ./satsolver.py
[picosat_ex]: ./picosat.py
[picosat_home]: http://fmv.jku.at/picosat/
