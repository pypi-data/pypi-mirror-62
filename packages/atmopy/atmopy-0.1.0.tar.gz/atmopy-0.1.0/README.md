<p align="center">
    <img src="docs/source/_static/logo.png">
</p>
<p align="center">
    <a href="https://github.com/jorgepiloto/atmopy" alt="atmopy">
        <img src="https://img.shields.io/badge/-atmopy%20%F0%9F%8C%8D-blue"/>
    </a>
    <a href="https://www.python.org" alt="python">
        <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"/>
    </a>
    <a href="https://github.com/jorgepiloto/amtmopy" alt="license">
        <img src="https://img.shields.io/github/license/jorgepiloto/atmopy"/>
    </a>
    <a href="https://travis-ci.com/jorgepiloto/atmopy" alt="travis">
        <img src="https://travis-ci.com/jorgepiloto/atmopy.svg?branch=master"/>
    </a>
    <a href="https://codecov.io/github/jorgepiloto/atmopy?branch=master" alt="codecov">
        <img src="https://img.shields.io/codecov/c/github/jorgepiloto/atmopy.svg"/>
    </a>
</p>

About
-----

Modelling the atmosphere is a complicated task since many variables play
a role on the different thermodynamic conditions: solar-fluxes, latitude
and longitude position, diffusion of the different gasses...

Since the early days of aviation and astronautics, scientists have tried
to develop different models which take into account all the previous
parameters in order to get the most accurate results. In particular, we
care about density since it is directly related to drag force and
therefore with orbital decay among time.

This package is not only a collection of atmospheric routines but also a
tribute to all those people who developed them during the early days of
astronautics.


Installation for developers
---------------------------

This Python package makes use of a tool called
\[Flit\](<https://flit.readthedocs.io/en/latest/index.html>). In order
to install the package in development mode, please run the following
commands:

1.  Execute pip flit install
2.  Move inside the atmopy repository folder and run
    flit install --symlink
3.  Run nox for checking that atmopy was installed as expected.

