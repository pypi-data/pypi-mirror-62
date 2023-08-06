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

######################################################################
# STRUCTURE - GSAS-II plugin
######################################################################
import sys, tempfile, site, os, pickle, traceback
import subprocess
from subprocess import CalledProcessError

GSAS_II_IS_DEVELOP = False if not "GSASIIDEVELOP" in os.environ.keys() else str(os.environ.get('GSASIIDEVELOP')) == "1"

if GSAS_II_IS_DEVELOP:
    gsasii_dirname = os.environ.get("GSAS-II-DIR")
    gsasii_temp_dir = os.environ.get("GSAS-II-TEMP-DIR")
else:
    platform = sys.platform

    if platform == "darwin":
        gsasii_dirname = os.path.join(site.getsitepackages()[0], "GSAS-II-WONDER")
    elif platform.startswith("win"):
        gsasii_dirname = os.path.join(site.getsitepackages()[1], "GSAS-II-WONDER")
    elif platform.startswith("linux"):
        gsasii_dirname = os.path.join(site.getsitepackages()[0], "GSAS-II-WONDER")

    gsasii_temp_dir = tempfile.gettempdir()

sys.path.insert(0, gsasii_dirname)

project_file = os.path.join(gsasii_temp_dir, "temp.gpx")

from PyQt5.QtCore import Qt, QSettings

GSASII_MODE_ONLINE   = 0
GSASII_MODE_EXTERNAL = 1

try:
    import GSASIIscriptable as G2sc

    G2sc.SetPrintLevel("none")

    print("GSAS-II found in ", gsasii_dirname)
except Exception as e:
    print("GSAS-II not available")

class GSASIIReflectionData:
    def __init__(self, h, k, l, pos, multiplicity, F2):
        self.h = int(h)
        self.k = int(k)
        self.l = int(l)
        self.pos = pos
        self.multiplicity = int(multiplicity)
        self.F2 = F2

    @classmethod
    def create_key(cls, h, k, l):
        return str(h) + str(k) + str(l)

    def get_key(self):
        return self.create_key(self.h, self.k, self.l)

    def get_intensity_factor(self):
        return self.F2*self.multiplicity

    def __str__(self):
        return str(self.h           ) + " "  + \
               str(self.k           ) + " "  + \
               str(self.l           ) + " "  + \
               "%7s"%str(round(self.pos,3)) + " "  + \
               "%2s"%str(self.multiplicity) + " "  + \
               "%10s"%str(round(self.F2, 3)) + " "  + \
               "%12s"%str(round(self.get_intensity_factor(),3))

class GSASIIReflectionList:
    def __init__(self, cif_file, wavelength, twotheta_min=0.0, twotheta_max=180.0):
        self.__data = {}

        GSASII_MODE = QSettings().value("output/wonder-default-gsasii-mode", GSASII_MODE_ONLINE, int)

        if GSASII_MODE == GSASII_MODE_ONLINE:
            gpx = G2sc.G2Project(newgpx=project_file)
            gpx.add_phase(cif_file, phasename="wonder_phase", fmthint='CIF')

            hist1 = gpx.add_simulated_powder_histogram("wonder_histo",
                                                       self.create_temp_prm_file(wavelength),
                                                       twotheta_min,
                                                       twotheta_max,
                                                       0.01,
                                                       phases=gpx.phases())

            gpx.data['Controls']['data']['max cyc'] = 0 # refinement not needed
            gpx.do_refinements([{}])

            gsasii_data = hist1.reflections()["wonder_phase"]["RefList"]

            for item in gsasii_data:
                entry = GSASIIReflectionData(item[0], item[1], item[2], item[5], item[3], item[9])
                self.__data[entry.get_key()] = entry

        elif GSASII_MODE == GSASII_MODE_EXTERNAL:
            try:
                pipe = subprocess.Popen([sys.executable, self.create_python_script(gsasii_dirname,
                                                                                   gsasii_temp_dir,
                                                                                   os.path.join(gsasii_temp_dir, "gsasii_data.dat"),
                                                                                   project_file,
                                                                                   cif_file,
                                                                                   self.create_temp_prm_file(wavelength),
                                                                                   twotheta_min,
                                                                                   twotheta_max)], stdout=subprocess.PIPE)

                gsasii_data = pickle.loads(pipe.stdout.read())
            except CalledProcessError as error:
                raise Exception("Failed to call GSAS-II: " + ''.join(traceback.format_tb(error.__traceback__)))

            for item in gsasii_data:
                entry = GSASIIReflectionData(item[0], item[1], item[2], item[5], item[3], item[9])
                self.__data[entry.get_key()] = entry

    def get_reflection(self, h, k, l):
        return self.__data[GSASIIReflectionData.create_key(h, k, l)]

    def get_reflections(self):
        return [self.__data[key] for key in self.__data.keys()]

    @classmethod
    def create_temp_prm_file(cls, wavelength, with_error_profile=False):
        temp_file_name = os.path.join(gsasii_temp_dir, "temp.instprm")
        temp_file = open(temp_file_name, "w")

        if with_error_profile: # 11-BM @ APS-ANL
            text = "#GSAS-II instrument parameter file; do not add/delete items!\n" + \
                   "Type: PXC" + "\n" + \
                   "Bank: 1.0" + "\n" + \
                   "Lam: " + "{:10.8f}".format(wavelength*10) + "\n" + \
                   "Polariz.: 0.99" + "\n" + \
                   "Azimuth: 0.0" + "\n" + \
                   "Zero: 0.0" + "\n" + \
                   "U: 1.163" + "\n" + \
                   "V: -0.126" + "\n" + \
                   "W: 0.063" + "\n" + \
                   "X: 0.0" + "\n" + \
                   "Y: 0.0" + "\n" + \
                   "Z: 0.0" + "\n" + \
                   "SH / L: 0.002"
        else:
            text = "#GSAS-II instrument parameter file; do not add/delete items!\n" + \
                   "Type: PXC" + "\n" + \
                   "Bank: 1.0" + "\n" + \
                   "Lam: " + "{:10.8f}".format(wavelength*10) + "\n" + \
                   "Polariz.: 0.99" + "\n" + \
                   "Azimuth: 0.0" + "\n" + \
                   "Zero: 0.0" + "\n" + \
                   "U: 0.0" + "\n" + \
                   "V: 0.0" + "\n" + \
                   "W: 0.0" + "\n" + \
                   "X: 0.0" + "\n" + \
                   "Y: 0.0" + "\n" + \
                   "Z: 0.0" + "\n" + \
                   "SH / L: 0.0"

        temp_file.write(text)
        temp_file.close()

        return temp_file_name

    def create_python_script(self, gsasii_dirname, gsasii_temp_dir, gsasii_data_file, project_file, cif_file, prm_file, twotheta_min, twotheta_max):
        python_script_file_name = os.path.join(gsasii_temp_dir, "temp.py")
        python_script =  open(python_script_file_name, "w")

        text =  "import sys, os, pickle\n\n"  + \
                "sys.path.insert(0, '" + gsasii_dirname + "')\n" + \
                "gsasii_temp_dir = '" + gsasii_temp_dir + "'\n" + \
                "gsasii_data_file = '" + gsasii_data_file + "'\n" + \
                "project_file = '" + project_file + "'\n" + \
                "cif_file = '" + cif_file + "'\n" + \
                "prm_file = '" + prm_file + "'\n" + \
                "twotheta_min = " + str(twotheta_min) + "\n" + \
                "twotheta_max = " + str(twotheta_max) + "\n" + \
                "try:\n" + \
                "    import GSASIIscriptable as G2sc\n" + \
                "    G2sc.SetPrintLevel('none')\n" + \
                "except:\n" + \
                "    raise ValueError('GSAS NOT FOUND!')\n\n" + \
                "gpx = G2sc.G2Project(newgpx=project_file)\n" + \
                "gpx.add_phase(cif_file, phasename='wonder_phase', fmthint='CIF')\n" + \
                "hist1 = gpx.add_simulated_powder_histogram('wonder_histo', prm_file, twotheta_min, twotheta_max, 0.01, phases=gpx.phases())\n" + \
                "gpx.data['Controls']['data']['max cyc'] = 0\n" + \
                "gpx.do_refinements([{}])\n" + \
                "gsasii_data = hist1.reflections()['wonder_phase']['RefList']\n" + \
                "pickle.dump(gsasii_data, os.fdopen(sys.stdout.fileno(), 'wb'))"

        python_script.write(text)
        python_script.close()

        return python_script_file_name

from PyQt5.QtCore import QMutex

mutex = QMutex()

def gsasii_load_reflections(cif_file, wavelength, twotheta_min=0.0, twotheta_max=180.0):
    try:
        mutex.lock()

        gsasii_reflections = GSASIIReflectionList(cif_file, wavelength, twotheta_min, twotheta_max)

        mutex.unlock()

        return gsasii_reflections
    except Exception as e:
        mutex.unlock()

        raise e

def gsasii_intensity_factor(h, k, l, reflections):
    try:
        return reflections.get_reflection(h, k, l).get_intensity_factor()
    except:
        return 0

