# -*- coding: utf-8

"""Module for helper functions used by several other modules.

This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/tools/helpers.py

SPDX-License-Identifier: MIT
"""
from tespy.tools.global_vars import (
        err, molar_masses
        )

import CoolProp as CP

import numpy as np

import os
import logging


# %%


class TESPyNetworkError(Exception):
    """Custom message for network related errors."""

    pass


class TESPyConnectionError(Exception):
    """Custom message for connection related errors."""

    pass


class TESPyComponentError(Exception):
    """Custom message for component related errors."""

    pass

# %%


def newton(func, deriv, params, y, **kwargs):
    r"""
    Find zero crossings with 1-D newton algorithm.

    Parameters
    ----------
    func : function
        Function to find zero crossing in,
        :math:`0=y-func\left(x,\text{params}\right)`.

    deriv : function
        First derivative of the function.

    params : list
        Additional parameters for function, optional.

    y : float
        Target function value.

    val0 : float
        Starting value, default: val0=300.

    valmin : float
        Lower value boundary, default: valmin=70.

    valmax : float
        Upper value boundary, default: valmax=3000.

    max_iter : int
        Maximum number of iterations, default: max_iter=10.

    Returns
    -------
    val : float
        x-value of zero crossing.

    Note
    ----
    Algorithm

    .. math::

        x_{i+1} = x_{i} - \frac{f(x_{i})}{\frac{df}{dx}(x_{i})}\\
        f(x_{i}) \leq \epsilon
    """
    # default valaues
    x = kwargs.get('val0', 300)
    valmin = kwargs.get('valmin', 70)
    valmax = kwargs.get('valmax', 3000)
    max_iter = kwargs.get('max_iter', 10)

    # start newton loop
    res = 1
    i = 0
    while abs(res) >= err:
        # calculate function residual and new value
        res = y - func(params, x)
        x += res / deriv(params, x)

        # check for value ranges
        if x < valmin:
            x = valmin
        if x > valmax:
            x = valmax
        i += 1

        if i > max_iter:
            msg = ('Newton algorithm was not able to find a feasible value '
                   'for function ' + str(func) + '. Current value with x=' +
                   str(x) + ' is ' + str(func(params, x)) +
                   ', target value is ' + str(y) + '.')
            logging.debug(msg)

            break

    return x

# %%


def reverse_2d(params, y):
    r"""
    Calculate the residual value of an inverse function.

    Parameters
    ----------
    params : list
        Variable function parameters.

    y : float
        Function value of function :math:`y = f \left( x_1, x_2 \right)`.

    Returns
    -------
    deriv : float
        Residual value of inverse function :math:`x_2 - f\left(x_1, y \right)`.
    """
    func, x1, x2 = params[0], params[1], params[2]
    return x2 - func.ev(x1, y)


def reverse_2d_deriv(params, y):
    r"""
    Calculate derivative of an inverse function.

    Parameters
    ----------
    params : list
        Variable function parameters.

    y : float
        Function value of function :math:`y = f \left( x_1, x_2 \right)`,
        so that :math:`x_2 - f\left(x_1, y \right) = 0`

    Returns
    -------
    deriv : float
        Partial derivative :math:`\frac{\partial f}{\partial y}`.
    """
    func, x1 = params[0], params[1]
    return - func.ev(x1, y, dy=1)

# %%


def molar_mass_flow(flow):
    r"""
    Calculate molar mass flow.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    mm : float
        Molar mass flow mm / (mol/s).

        .. math::

            mm = \sum_{i} \left( \frac{x_{i}}{M_{i}} \right)
    """
    mm = 0
    for fluid, x in flow.items():
        if x > err:
            mm += x / molar_masses[fluid]
    return mm

# %%


def num_fluids(fluids):
    r"""
    Return number of fluids in fluid mixture.

    Parameters
    ----------
    fluids : dict
        Fluid mass fractions.

    Returns
    -------
    n : int
        Number of fluids in fluid mixture n / 1.

        .. math::

            n = \sum_{i} \left( \begin{cases}
            0 & x_{i} < \epsilon \\
            1 & x_{i} \geq \epsilon
            \end{cases} \right)\;
            \forall i \in \text{network fluids}
    """
    n = 0
    for fluid, x in fluids.items():
        if x > err:
            n += 1

    return n

# %%


def single_fluid(fluids):
    r"""
    Return the name of the pure fluid in a fluid vector.

    Parameters
    ----------
    fluids : dict
        Fluid mass fractions.

    Returns
    -------
    fluid : str
        Name of the single fluid.
    """
    if num_fluids(fluids) == 1:
        for fluid, x in fluids.items():
            if x > err:
                return fluid
    else:
        return []

# %%


def fluid_structure(fluid):
    r"""
    Return the checmical formula of fluid.

    Parameters
    ----------
    fluid : str
        Name of the fluid.

    Returns
    -------
    parts : dict
        Dictionary of the chemical base elements as keys and the number of
        atoms in a molecule as values.

    Example
    -------
    Get the chemical formula of methane.

    >>> from tespy.tools.helpers import fluid_structure
    >>> elements = fluid_structure('methane')
    >>> elements['C'], elements['H']
    (1, 4)
    """
    parts = {}
    for element in CP.CoolProp.get_fluid_param_string(
            fluid, 'formula').split('}'):
        if element != '':
            el = element.split('_{')
            parts[el[0]] = int(el[1])

    return parts

# %%


def lamb(re, ks, d):
    r"""
    Calculate the darcy friction factor from the moody diagram.

    Parameters
    ----------
    re : float
        Reynolds number re / 1.

    ks : float
        Pipe roughness ks / m.

    d : float
        Pipe diameter/characteristic lenght d / m.

    Returns
    -------
    lamb : float
        Darcy friction factor lamb / 1

    Note
    ----
    **Laminar flow** (:math:`re \leq 2320`)

    .. math::
        \lambda = \frac{64}{re}

    **turbulent flow** (:math:`re > 2320`)

    *hydraulically smooth:* :math:`\frac{re \cdot k_{s}}{d} < 65`

    .. math::
        \lambda = \begin{cases}
        0.03164 \cdot re^{-0.25} & re \leq 10^5\\
        0.0032 + 0.221 \cdot re^{-0.237} & 10^5 < re < 5 \cdot 10^6\\
        solve \left(0 = 2 \cdot \log\left(re \cdot \sqrt{\lambda} \right) -0.8
        - \frac{1}{\sqrt{\lambda}}\right) & re \geq 5 \cdot 10^6 \\
        \end{cases}

    *transition zone:* :math:`65 \leq \frac{re \cdot k_{s}}{d} \leq 1300`

    .. math::
        \lambda = solve \left( 0 = 2 \cdot \log \left( \frac{2.51}{re \cdot
        \sqrt{\lambda}} + \frac{k_{s}}{d} \cdot 0.269 \right) -
        \frac{1}{\sqrt{\lambda}} \right)

    *hydraulically rough:* :math:`\frac{re \cdot k_{s}}{d} > 1300`

    .. math::
        \lambda = \frac{1}{\left( 2\cdot \log \left( \frac{3.71 \cdot d}{k_{s}}
        \right) \right)}

    Example
    -------
    Calculate the friction coefficient used in the Darcy-Weisbach-equation at
    different hydraulic states.

    >>> from tespy.tools.helpers import lamb
    >>> ks = 5e-5
    >>> d = 0.05
    >>> re_laminar = 2000
    >>> re_turb_smooth = 20000
    >>> re_turb_trans = 70000
    >>> re_high = 1000000
    >>> d_high = 0.8
    >>> re_very_high = 6000000
    >>> d_very_high = 1
    >>> ks_low = 1e-5
    >>> ks_rough = 1e-3
    >>> lamb(re_laminar, ks, d)
    0.032
    >>> round(lamb(re_turb_smooth, ks, d), 3)
    0.027
    >>> round(lamb(re_turb_trans, ks, d), 3)
    0.023
    >>> round(lamb(re_turb_trans, ks_rough, d), 3)
    0.049
    >>> round(lamb(re_high, ks, d_high), 3)
    0.012
    >>> round(lamb(re_very_high, ks_low, d_very_high), 3)
    0.009
    """
    if re <= 2320:
        return 64 / re
    else:
        if re * ks / d < 65:
            if re <= 1e5:
                return 0.3164 * re ** (-0.25)
            elif re > 1e5 and re < 5e6:
                return 0.0032 + 0.221 * re ** (-0.237)
            else:
                l0 = 0.02
                return newton(lamb_smooth, dlamb_smooth_dlamb, [re],
                              0, val0=l0, valmin=0.00001, valmax=0.2)

        elif re * ks / d > 1300:
            return 1 / (-2 * np.log10(ks / (3.71 * d))) ** 2

        else:
            l0 = 0.002
            return newton(lamb_trans, dlamb_trans_dlamb, [re, ks, d], 0,
                          val0=l0, valmin=0.0001, valmax=0.2)


def lamb_smooth(params, lamb):
    """Calculate lambda in smooth conditions."""
    re = params[0]
    return 2 * np.log10(re * lamb ** 0.5) - 0.8 - 1 / lamb ** 0.5


def dlamb_smooth_dlamb(params, lamb):
    """Calculate derivative of lambda in smooth conditions."""
    return 1 / (lamb * np.log(10)) + 1 / 2 * lamb ** (-1.5)


def lamb_trans(params, lamb):
    """Calculate lambda in transition region (smooth to rough)."""
    re, ks, d = params[0], params[1], params[2]
    return (2 * np.log10(2.51 / (re * lamb ** 0.5) + ks / (3.71 * d)) +
            1 / lamb ** 0.5)


def dlamb_trans_dlamb(params, lamb):
    """Calculate derivative for lambda in transition region."""
    d = 0.001
    return (lamb_trans(params, lamb + d) -
            lamb_trans(params, lamb - d)) / (2 * d)

# %%


def modify_path_os(path):
    """
    Modify a path according the os.

    Also detects weather the path specification is absolute or relative and
    adjusts the path respectively.

    Parameters
    ----------
    path : str
        Path to modify.

    Returns
    -------
    path : str
        Modified path.
    """
    if os.name == 'nt':
        # windows
        path = path.replace('/', '\\')
        if path[0] != '\\' and path[1:2] != ':' and path[0] != '.':
            # relative path
            path = '.\\' + path
    else:
        # linux, mac
        path = path.replace('\\', '/')
        if path[0] != '/' and path[0] != '.':
            # relative path
            path = './' + path

    return path

# %%


def get_basic_path():
    """
    Return the basic tespy path and creates it if necessary.

    The basic path is the '.tespy' folder in the $HOME directory.
    """
    basicpath = os.path.join(os.path.expanduser('~'), '.tespy')
    if not os.path.isdir(basicpath):
        os.mkdir(basicpath)
    return basicpath


def extend_basic_path(subfolder):
    """
    Return a path based on the basic tespy path and creates it if necessary.

    The subfolder is the name of the path extension.
    """
    extended_path = os.path.join(get_basic_path(), subfolder)
    if not os.path.isdir(extended_path):
        os.mkdir(extended_path)
    return extended_path
