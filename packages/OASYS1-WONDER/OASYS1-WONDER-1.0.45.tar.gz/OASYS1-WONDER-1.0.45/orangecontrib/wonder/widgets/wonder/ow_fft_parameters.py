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

import sys

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QDoubleValidator

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget
from orangecontrib.wonder.util.gui_utility import gui
from oasys.widgets import congruence
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters
from orangecontrib.wonder.fit.parameters.initialization.fft_parameters import FFTInitParameters, FFTTypes


class OWFFTParameters(OWGenericWidget):

    name = "FFT Parameters"
    description = "Define FFT Parameters"
    icon = "icons/fft_parameters.png"
    priority = 2

    want_main_area = False

    s_max = Setting(9.0)
    n_step = Setting(3)
    fft_type = Setting(0)

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters)]

    def __init__(self):
        super().__init__(show_automatic_box=True)

        self.setFixedHeight(310)

        main_box = gui.widgetBox(self.controlArea,
                                 "Fit Initialization", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 10, height=210)

        button_box = gui.widgetBox(main_box,
                                   "", orientation="horizontal",
                                   width=self.CONTROL_AREA_WIDTH-25)

        gui.button(button_box,  self, "Send Fit Initialization", height=40, callback=self.send_fit_initialization)

        fft_box = gui.widgetBox(main_box,
                                 "FFT", orientation="vertical",
                                 width=self.CONTROL_AREA_WIDTH - 30)

        gui.lineEdit(fft_box, self, "s_max", "S_max [nm-1]", labelWidth=250, valueType=float, validator=QDoubleValidator())

        self.cb_n_step = orangegui.comboBox(fft_box, self, "n_step", label="FFT Steps", labelWidth=350, items=["1024", "2048", "4096", "8192", "16384", "32768", "65536"], sendSelectedValue=True, orientation="horizontal")
        orangegui.comboBox(fft_box, self, "fft_type", label="FFT Type", items=FFTTypes.tuple(), orientation="horizontal")

        orangegui.rubber(self.controlArea)

        runaction = OWAction("Send Fit Initialization", self)
        runaction.triggered.connect(self.send_fit_initialization)
        self.addAction(runaction)

    def send_fit_initialization(self):
        try:
            if not self.fit_global_parameters is None:
                congruence.checkStrictlyPositiveNumber(self.s_max, "S Max")

                self.fit_global_parameters.fit_initialization.fft_parameters = FFTInitParameters(s_max=self.s_max,
                                                                                                 n_step=int(self.cb_n_step.currentText()),
                                                                                                 fft_type=self.fft_type)
                self.fit_global_parameters.regenerate_parameters()

                self.send("Fit Global Parameters", self.fit_global_parameters)

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def set_data(self, data):
        if not data is None:
            self.fit_global_parameters = data.duplicate()

            if not self.fit_global_parameters.fit_initialization.fft_parameters is None:
                self.n_step = ((self.fit_global_parameters.fit_initialization.fft_parameters.n_step)/1024)-1
                self.s_max = self.fit_global_parameters.fit_initialization.fft_parameters.s_max
                self.fft_type = self.fit_global_parameters.fit_initialization.fft_parameters.fft_type

            if self.is_automatic_run:
                self.send_fit_initialization()



if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWFFTParameters()
    ow.show()
    a.exec_()
    ow.saveSettings()
