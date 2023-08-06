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
import inspect

from oasys.widgets import congruence
from orangecontrib.wonder.util.fit_utilities import Utilities
from orangecontrib.wonder.fit.parameters.fit_parameter import ParametersList

#---------------------------------------
# DATA STRUCTURES
#---------------------------------------
class DiffractionPoint:
    twotheta = None
    intensity = None
    error = None
    s = None

    def __init__ (self,
                  twotheta = None,
                  intensity = None,
                  error = None,
                  s = None):
        self.twotheta = twotheta
        self.intensity = intensity
        self.error = error
        self.s = s

        self._check_attributes_congruence()

    def apply_wavelength(self, wavelength):
        if self.twotheta is None:
            self.twotheta = self._get_twotheta_from_s(self.s, wavelength)
        elif self.s is None:
            self.s = self._get_s_from_twotheta(self.twotheta, wavelength)

    def get_array (self):
        return numpy.array([self.twotheta, self.intensity, self.error, self.s])

    @classmethod
    def _get_s_from_twotheta(cls, twotheta, wavelength):
        if twotheta is None: return None

        return Utilities.s(theta=numpy.radians(twotheta/2),
                           wavelength=wavelength.value)

    @classmethod
    def _get_twotheta_from_s(cls, s, wavelength):
        if s is None: return None

        return numpy.degrees(2*Utilities.theta(s, wavelength.value))

    def _check_attributes_congruence(self):
        if not self.s is None:
            congruence.checkPositiveNumber(self.s, "s")
        if not self.twotheta is None:
            congruence.checkPositiveNumber(self.twotheta, "twotheta")

class DiffractionPattern(ParametersList):
    diffraction_pattern = None
    name = ""

    @classmethod
    def get_parameters_prefix(cls):
        return "diffraction_pattern_"

    @classmethod
    def get_default_name(cls, diffraction_pattern_index=0):
        return "Diff. Patt. " + str(diffraction_pattern_index + 1)

    def __init__(self, n_points = 0, name=""):
        if n_points > 0:
            self.diffraction_pattern = numpy.full(n_points, None)
        else:
            self.diffraction_pattern = None

        self.name = name

    def add_diffraction_point (self, diffraction_point):
        if diffraction_point is None: raise ValueError ("Diffraction Point is None")
        if not isinstance(diffraction_point, DiffractionPoint): raise ValueError ("diffraction point should be of type Diffraction Point")

        if self.diffraction_pattern is None:
            self.diffraction_pattern = numpy.array([diffraction_point])
        else:
            self.diffraction_pattern = numpy.append(self.diffraction_pattern, diffraction_point)

    def set_diffraction_point(self, index, diffraction_point):
        self.__check_diffraction_pattern()
        self.diffraction_pattern[index] = diffraction_point

    def diffraction_points_count(self):
        return 0 if self.diffraction_pattern is None else len(self.diffraction_pattern)

    def get_diffraction_point(self, index):#
        self.__check_diffraction_pattern()

        return self.diffraction_pattern[index]

    def apply_wavelength(self, wavelength):
        if not wavelength is None:
            for diffraction_point in self.diffraction_pattern:
                diffraction_point.apply_wavelength(wavelength)
        else:
            raise ValueError("wavelength is None")

    def duplicate(self):
        self.__check_diffraction_pattern()

        return super(DiffractionPattern, self).duplicate()

    def tuples(self):
        data = [[diffraction_point.twotheta, diffraction_point.intensity,diffraction_point.error, diffraction_point.s] for diffraction_point in self.diffraction_pattern]
        data = numpy.array(data)

        return data[:, 0], data[:, 1], data[:, 2], data[:, 3]

    def get_name(self, diffraction_pattern_index=0):
        try:
            congruence.checkEmptyString(self.name, "--")

            return self.name.strip()
        except:
            return DiffractionPattern.get_default_name(diffraction_pattern_index)

    # "PRIVATE METHODS"
    def __check_diffraction_pattern(self):
        if self.diffraction_pattern is None:
            raise AttributeError("diffraction pattern is "
                                 "not initialized")

# ----------------------------------------------------
#  FACTORY METHOD
# ----------------------------------------------------

class DiffractionPatternLimits:
    def __init__(self, twotheta_min = -numpy.inf, twotheta_max = numpy.inf):
        self.twotheta_max = twotheta_max
        self.twotheta_min = twotheta_min


class DiffractionPatternFactory:
    @classmethod
    def create_diffraction_pattern_from_file(clscls, file_name, limits=None, name=""):
        return DiffractionPatternFactoryChain.Instance().create_diffraction_pattern_from_file(file_name, limits, name)

import os

# ----------------------------------------------------
#  CHAIN OF RESPONSABILITY
# ----------------------------------------------------

class DiffractionPatternFactoryInterface():
    def create_diffraction_pattern_from_file(self, file_name, limits=None, name=""):
        raise NotImplementedError ("Method is Abstract")

    def _get_extension(self, file_name):
        filename, file_extension = os.path.splitext(file_name)
        return file_extension

from orangecontrib.wonder.util import Singleton

import sys

def predicate(class_name):
    return inspect.isclass(class_name) and issubclass(class_name, DiffractionPatternFactoryHandler)

@Singleton
class DiffractionPatternFactoryChain(DiffractionPatternFactoryInterface):
    _chain_of_handlers = []

    def __init__(self):
        self.initialize_chain()

    def initialize_chain(self):
        self._chain_of_handlers = []

        for handler in self._get_handlers_list():
            self._chain_of_handlers.append((globals()[handler])())

    def append_handler(self, handler = None):
        if self._chain_of_handlers is None: self.initialize_chain()

        if handler is None:
            raise ValueError ("Handler is None")

        if not isinstance(handler, DiffractionPatternFactoryHandler):
            raise ValueError("Handler Type not correct")

        self._chain_of_handlers.append(handler)

    def create_diffraction_pattern_from_file(self, file_name, limits=None, name=""):
        file_extension = self._get_extension(file_name)

        for handler in self._chain_of_handlers:
            if handler.is_handler(file_extension):
                return handler.create_diffraction_pattern_from_file(file_name, limits, name)

        raise ValueError ("File Extension not recognized")

    def _get_handlers_list(self):
        classes = numpy.array([m[0] for m in inspect.getmembers(sys.modules[__name__], predicate)])

        return numpy.asarray(classes[numpy.where(classes != "DiffractionPatternFactoryHandler")])

# ---------------------------------------------------
# HANDLERS INTERFACE
# ---------------------------------------------------

class DiffractionPatternFactoryHandler(DiffractionPatternFactoryInterface):

    def _get_handled_extension(self):
        raise NotImplementedError()

    def is_handler(self, file_extension):
        return file_extension == self._get_handled_extension()

# ---------------------------------------------------
# HANDLERS
# ---------------------------------------------------

class DiffractionPatternXyeFactoryHandler(DiffractionPatternFactoryHandler):

    def _get_handled_extension(self):
        return ".xye"

    def create_diffraction_pattern_from_file(self, file_name, limits=None, name=""):
        return DiffractionPatternXye(file_name = file_name, limits=limits, name=name)

class DiffractionPatterXyFactoryHandler(DiffractionPatternXyeFactoryHandler):

    def _get_handled_extension(self):
        return ".xy"

class DiffractionPatternRawFactoryHandler(DiffractionPatternFactoryHandler):

    def _get_handled_extension(self):
        return ".raw"

    def create_diffraction_pattern_from_file(self, file_name, limits=None, name=""):
        return DiffractionPatternRaw(file_name= file_name, limits=limits, name=name)


# ----------------------------------------------------
# PERSISTENCY MANAGAMENT
# ----------------------------------------------------

class DiffractionPatternXye(DiffractionPattern):
    def __init__(self, file_name= "", limits=None, name=""):
        super(DiffractionPatternXye, self).__init__(n_points=0, name=name)

        self.__initialize_from_file(file_name, limits)

    def __initialize_from_file(self, file_name, limits):
        #method supposes only 2 rows of header are present
        #can be changed. Right now I want to finish
        with open(file_name, 'r') as xyefile : lines = xyefile.readlines()
        n_points = len(lines) - 2
        if n_points > 0:
            if len(lines) < 3: raise Exception("Number of lines in file < 3: wrong file format")
            if limits is None: self.diffraction_pattern = numpy.array([None] *n_points)

            for i in numpy.arange(2, n_points+2):
                line = lines[i].split()

                if len(line) < 2 : raise  Exception("Number of columns in line " + str(i) + " < 2: wrong file format")

                twotheta = float(line[0])
                intensity = float(line[1])

                if len(line) >= 3:
                    error = float(line[2])
                else:
                    error = numpy.sqrt(intensity)

                if limits is None:
                    self.set_diffraction_point(index=i-2,
                                               diffraction_point=DiffractionPoint(twotheta=twotheta,
                                                                                  intensity=intensity,
                                                                                  error=error))
                elif  limits.twotheta_min <= twotheta <= limits.twotheta_max:
                    self.add_diffraction_point(diffraction_point=DiffractionPoint(twotheta=twotheta,
                                                                                  intensity=intensity,
                                                                                  error=error))

class DiffractionPatternRaw(DiffractionPattern):
    def __init__(self, file_name= "", wavelength=None, limits=None, name=""):
        super(DiffractionPatternRaw, self).__init__(n_points = 0, name=name)

        self.__initialize_from_file(file_name, limits)

    def __initialize_from_file(self, file_name, limits):
        #method supposes only 1 rows of header is present
        #can be changed.
        with open(file_name, 'r') as rawfile : lines = rawfile.readlines()

        splitted_row = lines[1].split(sep=',')

        if not len(splitted_row) == 5:
            splitted_row = numpy.array(lines[1].split(sep=' '))
            splitted_row = splitted_row[numpy.where(splitted_row != '')]

        n_points = int(splitted_row[0])
        step = float(splitted_row[1])
        starting_theta = float(splitted_row[2])

        if limits is None: self.diffraction_pattern = numpy.array([None] *n_points)

        for i in numpy.arange(2, n_points+2):
            index = i-2
            line = lines[i]

            intensity = float(line)
            error = numpy.sqrt(intensity)

            if limits is None:
                self.set_diffraction_point(index,
                                           diffraction_point= DiffractionPoint(twotheta=starting_theta + step*index,
                                                                               intensity=intensity,
                                                                               error=error))
            else:
                twotheta = starting_theta + step*index

                if  limits.twotheta_min <= twotheta <= limits.twotheta_max:
                    self.add_diffraction_point(diffraction_point=DiffractionPoint(twotheta=twotheta,
                                                                                  intensity=intensity,
                                                                                  error=error))
