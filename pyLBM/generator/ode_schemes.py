from __future__ import print_function
# Authors:
#     Loic Gouarin <loic.gouarin@math.u-psud.fr>
#     Benjamin Graille <benjamin.graille@math.u-psud.fr>
#
# License: BSD 3 clause

import numpy as np
import re
from ..logs import setLogger

class ode_solver():
    """
    generic class for the ode solver
    """
    def __init__(self):
        self.log = setLogger(__name__)
        self.code = ''
        self.nb_of_floors = 0
    def parameters(self, indices_m, f, dt, indent = '', add_copy=''):
        self.indices_m = indices_m
        self.f = f
        self.dt = dt
        self.indent = indent
        self.add_copy = add_copy
    def verification(self):
        n, m = self.tbl.shape
        if n != m or n != self.nb_of_floors+1:
            self.log.error('Problem of size in the definition of the ode solver.')
    def __str__(self):
        return str(self.nb_of_floors)
    def cpt_code(self):
        N = len(self.indices_m)
        for nfi in range(self.nb_of_floors):
            for l in range(N):
                k = self.indices_m[l][0]
                i = self.indices_m[l][1]
                self.code += self.indent + "dummy{3:1d}[{0}] = m[{1}][{2}]".format(l, k, i, nfi) + self.add_copy + "\n"
                for nfj in range(nfi):
                    if self.tbl[nfi, nfj+1] != 0:
                        self.code += self.indent + "dummy{0:1d}[{1}] += ".format(nfi, l)
                        filj = self.f[l]
                        for ll in range(N):
                            kk = self.indices_m[ll][0]
                            ii = self.indices_m[ll][1]
                            filj = re.sub("m\[{0}\]\[{1}\]".format(kk,ii), "dummy{1:1d}[{0}]".format(ll, nfj), filj)
                        self.code += "{0:.15f}*{1}*(".format(self.tbl[nfi,0],  self.dt) + filj + ")\n"
                for nfj in range(nfi, self.nb_of_floors):
                    if self.tbl[nfi, nfj+1] != 0:
                        self.log.error('Implicit ode scheme are not allowed')
        for l in range(N):
            k = self.indices_m[l][0]
            i = self.indices_m[l][1]
            self.code += self.indent + "m[{0}][{1}] += ".format(k, i) + self.dt + "*("
            cpt_dummy = True
            for nfj in range(self.nb_of_floors):
                wj = self.tbl[self.nb_of_floors, nfj+1]
                if  wj != 0:
                    filj = self.f[l]
                    for ll in range(N):
                        kk = self.indices_m[ll][0]
                        ii = self.indices_m[ll][1]
                        filj = re.sub("m\[{0}\]\[{1}\]".format(kk,ii), "dummy{1:1d}[{0}]".format(ll, nfj), filj)
                    if cpt_dummy or wj<0:
                        add_dummy = ''
                    else:
                        add_dummy = "+"
                    cpt_dummy = False
                    self.code += add_dummy + "{0:.15f}*(".format(wj) + filj + ")"
            self.code += ")\n"
        return self.code


class basic(ode_solver):
    """
    basic ode solver with no Runge-Kutta formalism
    no dummy variables -> more efficient
    """
    def __init__(self):
        ode_solver.__init__(self)
    def cpt_code(self):
        for l in range(len(self.indices_m)):
            k = self.indices_m[l][0]
            i = self.indices_m[l][1]
            self.code += self.indent + "m[{0}][{1}] += ".format(k, i) + self.dt + "*(" + self.f[l] + ")\n"
        return self.code


class explicit_euler(ode_solver):
    """
    explicit Euler solver (1st order accuracy)
    formalism of Runge-Kutta solvers
    """
    def __init__(self):
        ode_solver.__init__(self)
        self.nb_of_floors = 1
        self.tbl = np.array([[0, 0], [0, 1]])
        self.verification()


class heun(ode_solver):
    """
    Heun solver (2nd order accuracy)
    formalism of Runge-Kutta solvers
    """
    def __init__(self):
        ode_solver.__init__(self)
        self.nb_of_floors = 2
        self.tbl = np.array([[0, 0, 0], [1, 1, 0], [0, 0.5, 0.5]])
        self.verification()


class middle_point(ode_solver):
    """
    middle point solver (2nd order accuracy)
    formalism of Runge-Kutta solvers
    """
    def __init__(self):
        ode_solver.__init__(self)
        self.nb_of_floors = 2
        self.tbl = np.array([[0, 0, 0], [0.5, 0.5, 0], [0, 0, 1]])
        self.verification()


class RK4(ode_solver):
    """
    RK4 solver (4th order accuracy)
    formalism of Runge-Kutta solvers
    """
    def __init__(self):
        ode_solver.__init__(self)
        self.nb_of_floors = 4
        self.tbl = np.array([
            [0, 0, 0, 0, 0],
            [0.5, 0.5, 0, 0, 0],
            [0.5, 0, 0.5, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1./6, 1./3, 1./3, 1./6]])
        self.verification()
