This presents the code to plot trajectories for the lake problem, as detailed on the following blog post:
https://waterprogramming.wordpress.com/2017/11/15/animations-2-2/

It uses the moviepy library, available with the command:
'pip install moviepy'

The three .py files are:
=> movie1.py and movie2.py which each produce a GIF when run; both call
=> attractors.py to compute the stable and unstable equilibria of the lake problem under a range of input levels

WARNING: attractors.py requires that the exponent q in the lake dynamics is an integer. 
Otherwise, the python tools to look for roots have problems around bifurcation points.

### License
Copyright (C) 2017 Charles Rougé, under the [MIT license](LICENSE.md).
