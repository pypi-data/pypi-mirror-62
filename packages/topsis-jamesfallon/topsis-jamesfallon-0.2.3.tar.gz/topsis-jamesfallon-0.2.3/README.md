# TOPSIS-Python

Inspired by [TOPSIS-Python](https://github.com/Glitchfix/TOPSIS-Python)
(python2).

Our python 3 code follows the same structure, defining a topsis class, 
but uses numpy linear algebra in order to modernise, optimise, and remove
redundant code.

## What is TOPSIS

**T**echnique for **O**rder **P**reference by **S**imilarity to **I**deal
**S**olution (TOPSIS) originated in the 1980s as a multi-criteria decision
making method. TOPSIS chooses the alternative of shortest Euclidean distance
from the ideal solution, and farthest distance from the negative-ideal
solution. More details at [wikipedia](https://en.wikipedia.org/wiki/TOPSIS). The
TOPSIS algorithm is succinctly explained in this [paper comparing TOPSIS and
VIKOR methods
](https://www.sciencedirect.com/science/article/pii/S0377221703000201)

## Using TOPSIS-Python

TOPSIS-Python can be run as in the following example:

```
>>> from topsis import topsis
>>> a = [[7, 9, 9, 8], [8, 7, 8, 7], [9, 6, 8, 9], [6, 7, 8, 6]]
>>> w = [0.1, 0.4, 0.3, 0.2]
>>> I = [1, 1, 1, 0]
>>> decision = topsis(a, w, I)
```

The decision matrix (`a`) should be constructed with each row representing
an alternative, and each column representing a criterion. We have used an
example given in [TOPSIS Method in MADM (Dr. Farhad Faez)](
http://www.faez.ir/CourseFile/TOPSIS.pdf)

Weights (`w`) is not already normalised will be normalised upon
initialisation. Information on benefit (1) cost (0) criteria should be provided
in `I`. 

By default, the optimisation (TOPSIS calculation) does not take place. No values
are stored in `decision.C` or `decision.optimum_choice`.

These can be calculated, either by calling `decision.calc()`, or by calling a
representation of the decision (which will itself call `decision.calc()`):

```
>>> decision

Alternatives ranking C:
[0.74269409 0.40359933 0.17586999 0.44142927]

Best alternative
a[0]: [7. 9. 9. 8.]

```

The rankings are saved in `decision.C`, with the highest ranking $`0.74269409`$
offering us the best decision, and lowest ranking $`0.17586999`$ offering the
worst decision making, according to TOPSIS method.

We are also then shown the best alternative index (which happens to be index 0
in this example), and the associated criteria coefficients of this alternative.

## Installation

The module can be installed from pypi using pip, or downloaded and installed
directly from git

pypi: <https://pypi.org/project/topsis-jamesfallon>
git: <https://gitlab.com/jamesfallon/topsis-python.git>


### pip

Installation with pip can be achieved in one line:

```
pip install topsis-jamesfallon
```


### Anaconda

If you are using anaconda, make sure that you are using your environment's
`pip`, and not the OS default. Your installation **only if using anaconda** may
look like:

1. Activate your environment

```
(base) $ conda activate custom_env
```

2. Ensure pip is installed in your environment

```
(custom_env) $ conda install pip
```

3. Make sure you are using your environment's pip installation. If not, you can always prepend the full path before the pip command.

```
(custom_env) $ which pip
.../path_to_your_anaconda_installation/anaconda3/envs/custom_env/bin/pip
```

4. Now install topsis from pypi

```
(custom_env) $ pip install topsis-jamesfallon
Collecting topsis-jamesfallon
Installing collected packages: topsis-jamesfallon
Successfully installed topsis-jamesfallon-0.2
```
