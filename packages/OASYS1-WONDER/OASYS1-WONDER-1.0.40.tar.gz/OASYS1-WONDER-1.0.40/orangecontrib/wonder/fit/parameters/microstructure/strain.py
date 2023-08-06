#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #########################################################################
# Copyright (c) 2020, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2020. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import numpy

from orangecontrib.wonder.fit.parameters.fit_parameter import FitParameter, ParametersList, ActivableParametersList

class LaueGroup:

    laue_groups = {}
    laue_groups["-1"] = "1"
    laue_groups["2/m"] = "2"
    laue_groups["2/mmm"] = "3"
    laue_groups["4/m"] = "4"
    laue_groups["4/mmm"] = "5"
    laue_groups["-3R"] = "6"
    laue_groups["-31mR"] = "7"
    laue_groups["-3"] = "8"
    laue_groups["-3m1"] = "9"
    laue_groups["-31m"] = "10"
    laue_groups["6/m"] = "11"
    laue_groups["6/mmm"] = "12"
    laue_groups["m3"] = "13"
    laue_groups["m3m"] = "14"

    @classmethod
    def get_laue_id(cls, laue_group):
        return cls.laue_groups[laue_group]

    @classmethod
    def get_laue_group(cls, laue_id):
        for key, value in cls.laue_groups.items():
            if int(value) == laue_id:
                return key

    @classmethod
    def tuple(cls):
        return ["-1", "2/m", "2/mmm", "4/m", "4/mmm", "-3R", "-31mR", "-3", "-3m1", "-31m", "6/m", "6/mmm", "m3", "m3m"]

class InvariantPAH(ActivableParametersList):
    @classmethod
    def get_parameters_prefix(cls):
        return "invariant_"

    def __init__(self,
                 aa,
                 bb,
                 laue_id = 1,
                 e1  = None,
                 e2  = None,
                 e3  = None,
                 e4  = None,
                 e5  = None,
                 e6  = None,
                 e7  = None,
                 e8  = None,
                 e9  = None,
                 e10 = None,
                 e11 = None,
                 e12 = None,
                 e13 = None,
                 e14 = None,
                 e15 = None,
                 active = True):
        super(InvariantPAH, self).__init__(active)

        self.aa = aa
        self.bb = bb
        self.laue_id = laue_id

        self.e1  = e1
        self.e2  = e2
        self.e3  = e3
        self.e4  = e4
        self.e5  = e5
        self.e6  = e6
        self.e7  = e7
        self.e8  = e8
        self.e9  = e9
        self.e10 = e10
        self.e11 = e11
        self.e12 = e12
        self.e13 = e13
        self.e14 = e14
        self.e15 = e15

    def get_invariant(self, h, k, l):
        invariant = self.e1.value*(h**4)

        if not self.e2  is None: invariant += self.e2.value*(k**4)
        if not self.e3  is None: invariant += self.e3.value*(l**4)
        if not self.e4  is None: invariant += 2*(self.e4.value*(h**2)*(k**2))
        if not self.e5  is None: invariant += 2*(self.e5.value*(k**2)*(l**2))
        if not self.e6  is None: invariant += 2*(self.e6.value*(h**2)*(l**2))
        if not self.e7  is None: invariant += 4*(self.e7.value*(h**3)*k)
        if not self.e8  is None: invariant += 4*(self.e8.value*(h**3)*l)
        if not self.e9  is None: invariant += 4*(self.e9.value*(k**3)*h)
        if not self.e10 is None: invariant += 4*(self.e10.value*(k**3)*l)
        if not self.e11 is None: invariant += 4*(self.e11.value*(l**3)*h)
        if not self.e12 is None: invariant += 4*(self.e12.value*(l**3)*k)
        if not self.e13 is None: invariant += 4*(self.e13.value*(h**2)*k*l)
        if not self.e14 is None: invariant += 4*(self.e14.value*(k**2)*h*l)
        if not self.e15 is None: invariant += 4*(self.e15.value*(l**2)*h*k)

        return invariant

    def get_warren_plot(self, h, k, l, L_max=20):
        step = L_max/100
        L = numpy.arange(start=step, stop=L_max + step, step=step)

        from orangecontrib.wonder.fit.functions.wppm_functions import displacement_invariant_pah

        DL = displacement_invariant_pah(L, h, k, l, self.aa.value, self.bb.value, self.get_invariant(h, k, l))

        return L, DL

class InvariantPAHLaueGroup1(InvariantPAH):
    def __init__(self, aa, bb, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, active=True):
        super().__init__(aa, bb, 1, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup2(InvariantPAH):
    def __init__(self, aa, bb, e1, e2, e3, e4, e5, e6, e7, e9, e15, active=True):
        super().__init__(aa, bb, 2, e1, e2, e3, e4, e5, e6, e7, e9=e9, e15=e15, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup3(InvariantPAH):
    def __init__(self, aa, bb, e1, e2, e3, e4, e5, e6, e7, active=True):
        super().__init__(aa, bb, 3, e1, e2, e3, e4, e5, e6, e7, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup4(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e4, e6, e7, active=True):
        super().__init__(aa, bb, 4, e1, e3=e3, e4=e4, e6=e6, e7=e7, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup5(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e4, e6, active=True):
        super().__init__(aa, bb, 5, e1, e3=e3, e4=e4, e6=e6, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup6(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e4, e6, e7, e9, e15, active=True):
        super().__init__(aa, bb, 6, e1, e3=e3, e4=e4, e6=e6, e7=e7, e9=e9, e15=e15, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup7(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e4, e6, e7, e9, e15, active=True):
        super().__init__(aa, bb, 7, e1, e3=e3, e4=e4, e6=e6, e7=e7, e9=e9, e15=e15, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup8(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e4, e6, e7, e9, e15, active=True):
        super().__init__(aa, bb, 8, e1, e3=e3, e4=e4, e6=e6, e7=e7, e9=e9, e15=e15, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup9(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e6, e13, active=True):
        super().__init__(aa, bb, 9, e1, e3=e3, e6=e6, e13=e13, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup10(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e6, e13, active=True):
        super().__init__(aa, bb, 10, e1, e3=e3, e6=e6, e13=e13, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup11(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e6, active=True):
        super().__init__(aa, bb, 11, e1, e3=e3, e6=e6, active=active)
        raise NotImplementedError("TO BE CHECKED")

class InvariantPAHLaueGroup12(InvariantPAH):
    def __init__(self, aa, bb, e1, e3, e6, active=True):
        super().__init__(aa, bb, 12, e1, e3=e3, e6=e6, active=active)

class InvariantPAHCubic(InvariantPAH):
    def __init__(self, aa, bb, laue_id, e1, e4, active=True):

        if aa.parameter_name[-2:]=="aa":
            parameter_prefix = aa.parameter_name[:-2]
        else:
            parameter_prefix = InvariantPAH.get_parameters_prefix()

        super(InvariantPAHCubic, self).__init__(aa, bb, laue_id,
                                                e1=e1,
                                                e2=FitParameter(parameter_name=parameter_prefix + "e2",
                                                                value=e1.value,
                                                                function=True,
                                                                function_value=e1.parameter_name),
                                                e3=FitParameter(parameter_name=parameter_prefix + "e3",
                                                                value=e1.value,
                                                                function=True,
                                                                function_value=e1.parameter_name),
                                                e4=e4,
                                                e5=FitParameter(parameter_name=parameter_prefix + "e5",
                                                                value=e4.value,
                                                                function=True,
                                                                function_value=e4.parameter_name),
                                                e6=FitParameter(parameter_name=parameter_prefix+ "e6",
                                                                value=e4.value,
                                                                function=True,
                                                                function_value=e4.parameter_name),
                                                active=active)

class InvariantPAHLaueGroup13(InvariantPAHCubic):
    def __init__(self, aa, bb, e1, e4, active=True):
        super(InvariantPAHLaueGroup13, self).__init__(aa, bb, 13, e1, e4, active=active)

class InvariantPAHLaueGroup14(InvariantPAHCubic):
    def __init__(self, aa, bb, e1, e4, active=True):
        super(InvariantPAHLaueGroup14, self).__init__(aa, bb, 14, e1, e4, active=active)

class KrivoglazWilkensModel(ActivableParametersList):
    @classmethod
    def get_parameters_prefix(cls):
        return "kw_"

    def __init__(self,
                 rho= None,
                 Re = None,
                 Ae = None,
                 Be = None,
                 As = None,
                 Bs = None,
                 mix= None,
                 b  = None,
                 active = True):
        super(KrivoglazWilkensModel, self).__init__(active)

        self.rho = rho
        self.Re  = Re
        self.Ae  = Ae
        self.Be  = Be
        self.As  = As
        self.Bs  = Bs
        self.mix = mix
        self.b   = b

    def get_warren_plot(self, h, k, l, L_max=50):
        step = L_max/100
        L = numpy.arange(start=step, stop=L_max + step, step=step)

        from orangecontrib.wonder.fit.functions.wppm_functions import displacement_krivoglaz_wilkens

        DL = displacement_krivoglaz_wilkens(L, h, k, l,
                                            self.rho.value,
                                            self.Re.value,
                                            self.Ae.value,
                                            self.Be.value,
                                            self.As.value,
                                            self.Bs.value,
                                            self.mix.value,
                                            self.b.value)
        return L, DL


class WarrenModel(ActivableParametersList):
    @classmethod
    def get_parameters_prefix(cls):
        return "warren_"

    def __init__(self,
                 average_cell_parameter=None,
                 active=True):
        super(WarrenModel, self).__init__(active)

        self.average_cell_parameter = average_cell_parameter



