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

import sys, numpy, os, copy

from PyQt5.QtWidgets import QMessageBox, QScrollArea, QApplication, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QColor, QFont, QTextCursor, QIntValidator

from silx.gui.plot.PlotWindow import PlotWindow
from silx.gui.plot.LegendSelector import LegendsDockWidget
from silx.gui import qt

from orangewidget.settings import Setting
from orangewidget import gui as orangegui
from orangewidget.widget import OWAction
from oasys.widgets import congruence

from orangecontrib.wonder.widgets.gui.ow_generic_widget import OWGenericWidget, OW_IS_DEVELOP
from orangecontrib.wonder.util.gui_utility import gui, ConfirmDialog

from orangecontrib.wonder.fit.fitters.fitter_factory import FitterFactory, FitterName
from orangecontrib.wonder.fit.fitters.fitter import FeedbackManager

from orangecontrib.wonder.fit.parameters.fit_parameter import PARAM_HWMAX, PARAM_HWMIN
from orangecontrib.wonder.fit.parameters.fit_global_parameters import FitGlobalParameters, FreeOutputParameters
from orangecontrib.wonder.fit.parameters.instrument.instrumental_parameters import InstrumentalParameters
from orangecontrib.wonder.fit.parameters.instrument.lab6_tan_correction import Lab6TanCorrection
from orangecontrib.wonder.fit.parameters.instrument.caglioti import Caglioti
from orangecontrib.wonder.fit.functions.wppm_functions import Shape, caglioti_fwhm, caglioti_eta, delta_two_theta_lab6, \
    integral_breadth_instrumental_function, integral_breadth_size, integral_breadth_strain, integral_breadth_total

AUTOMATIC_RUNTIME_ONLY = 0
AUTOMATIC_OASYS_SETTING = 1

class OWFitter(OWGenericWidget):
    name = "Fitter"
    description = "Fitter"
    icon = "icons/fit.png"
    priority = 60

    want_main_area = True

    automatic_mode = QSettings().value("output/wonder-default-automatic", AUTOMATIC_OASYS_SETTING, int)

    if automatic_mode == AUTOMATIC_OASYS_SETTING:
        is_automatic_run = Setting(False)
    else:
        is_automatic_run = False

    if OW_IS_DEVELOP:
        fitter_name = Setting(1)
    else:
        fitter_name = Setting(0)

    n_iterations = Setting(5)
    is_incremental = Setting(1)
    current_iteration = 0
    free_output_parameters_text = Setting("")
    save_file_name = Setting("fit_output.dat")

    is_interactive = Setting(1)

    show_wss_gof = Setting(1)
    show_ipf = Setting(1)
    show_shift = Setting(1)
    show_size = Setting(1)
    show_warren = Setting(1)
    show_integral_breadth = Setting(1)

    horizontal_headers = ["Name", "Value", "Min", "Max", "Fixed", "Function", "Expression", "e.s.d."]

    inputs = [("Fit Global Parameters", FitGlobalParameters, 'set_data')]
    outputs = [("Fit Global Parameters", FitGlobalParameters),
               ("Fitted Instrumental Parameters", InstrumentalParameters)]

    fit_global_parameters = None
    initial_fit_global_parameters = None
    fitted_fit_global_parameters = None
    current_wss = []
    current_gof = []

    stop_fit = False
    fit_running = False

    thread_exception = None

    fwhm_autoscale = Setting([1])
    fwhm_xmin = Setting([0.0])
    fwhm_xmax = Setting([150.0])
    fwhm_ymin = Setting([0.0])
    fwhm_ymax = Setting([1.0])

    eta_autoscale = Setting([1])
    eta_xmin = Setting([0.0])
    eta_xmax = Setting([150.0])
    eta_ymin = Setting([0.0])
    eta_ymax = Setting([1.0])

    lab6_autoscale = Setting([1])
    lab6_xmin = Setting([0.0])
    lab6_xmax = Setting([150.0])
    lab6_ymin = Setting([-1.0])
    lab6_ymax = Setting([1.0])

    size_autoscale = Setting([1])
    size_xmin = Setting([0.0])
    size_xmax = Setting([150.0])

    x_ib           = None
    labels_ib      = None
    annotations_ib = None
    distributions  = None
    text_size      = None

    free_input_parameter_label = ""
    free_output_parameter_label = ""
    fixed_label = ""
    function_label = ""

    def __fix_attrs(self):
        if not isinstance(self.fwhm_autoscale, list) or len(self.fwhm_autoscale) != 0: self.fwhm_autoscale = [1]
        if not isinstance(self.fwhm_xmin, list) or len(self.fwhm_xmin) == 0: self.fwhm_xmin = [0.0]
        if not isinstance(self.fwhm_xmax, list) or len(self.fwhm_xmax) == 0: self.fwhm_xmax = [150.0]
        if not isinstance(self.fwhm_ymin, list) or len(self.fwhm_ymin) == 0: self.fwhm_ymin = [0.0]
        if not isinstance(self.fwhm_ymax, list) or len(self.fwhm_ymax) == 0: self.fwhm_ymax = [1.0]
        if not isinstance(self.eta_autoscale, list) or len(self.eta_autoscale) == 0: self.eta_autoscale = [1]
        if not isinstance(self.eta_xmin, list) or len(self.eta_xmin) == 0: self.eta_xmin = [0.0]
        if not isinstance(self.eta_xmax, list) or len(self.eta_xmax) == 0: self.eta_xmax = [150.0]
        if not isinstance(self.eta_ymin, list) or len(self.eta_ymin) == 0: self.eta_ymin = [0.0]
        if not isinstance(self.eta_ymax, list) or len(self.eta_ymax) == 0: self.eta_ymax = [1.0]
        if not isinstance(self.lab6_autoscale, list) or len(self.lab6_autoscale) == 0: self.lab6_autoscale = [1]
        if not isinstance(self.lab6_xmin, list) or len(self.lab6_xmin) == 0: self.lab6_xmin = [0.0]
        if not isinstance(self.lab6_xmax, list) or len(self.lab6_xmax) == 0: self.lab6_xmax = [150.0]
        if not isinstance(self.lab6_ymin, list) or len(self.lab6_ymin) == 0: self.lab6_ymin = [0.0]
        if not isinstance(self.lab6_ymax, list) or len(self.lab6_ymax) == 0: self.lab6_ymax = [1.0]

    def __fix_flags(self):
        self.is_incremental = OWGenericWidget.fix_flag(self.is_incremental)
        self.is_interactive = OWGenericWidget.fix_flag(self.is_interactive)
        self.show_wss_gof = OWGenericWidget.fix_flag(self.show_wss_gof)
        self.show_ipf = OWGenericWidget.fix_flag(self.show_ipf)
        self.show_shift = OWGenericWidget.fix_flag(self.show_shift)
        self.show_size = OWGenericWidget.fix_flag(self.show_size)
        self.show_warren = OWGenericWidget.fix_flag(self.show_warren)
        self.show_integral_breadth = OWGenericWidget.fix_flag(self.show_integral_breadth)

    def __init__(self):
        super().__init__(show_automatic_box=True)
        
        self.__fix_attrs()
        self.__fix_flags()

        main_box = gui.widgetBox(self.controlArea, "Fitter Setting", orientation="vertical", width=self.CONTROL_AREA_WIDTH)

        button_box = gui.widgetBox(main_box, "", orientation="vertical", width=self.CONTROL_AREA_WIDTH-15, height=70)

        button_box_1 = gui.widgetBox(button_box, "", orientation="horizontal")

        self.fit_button = gui.button(button_box_1,  self, "Fit", height=30, callback=self.do_fit)
        self.fit_button.setStyleSheet("color: #252468")
        font = QFont(self.fit_button.font())
        font.setBold(True)
        font.setPixelSize(18)
        self.fit_button.setFont(font)

        self.stop_fit_button = gui.button(button_box_1,  self, "STOP", height=30, callback=self.stop_fit)
        self.stop_fit_button.setStyleSheet("color: red")
        font = QFont(self.stop_fit_button.font())
        font.setBold(True)
        font.setItalic(True)
        self.stop_fit_button.setFont(font)

        button_box_2 = gui.widgetBox(button_box, "", orientation="horizontal")

        gui.button(button_box_2,  self, "Send Current Fit", height=30, callback=self.send_current_fit)
        gui.button(button_box_2,  self, "Save Data", height=30, callback=self.save_data)

        runaction = OWAction("Fit", self)
        runaction.triggered.connect(self.do_fit)
        self.addAction(runaction)

        runaction = OWAction("Stop", self)
        runaction.triggered.connect(self.stop_fit)
        self.addAction(runaction)

        runaction = OWAction("Send Current Fit", self)
        runaction.triggered.connect(self.send_current_fit)
        self.addAction(runaction)


        orangegui.separator(main_box)

        self.cb_fitter = orangegui.comboBox(main_box, self, "fitter_name", label="Fit algorithm", items=FitterName.tuple(), orientation="horizontal")

        iteration_box = gui.widgetBox(main_box, "", orientation="horizontal", width=250)

        gui.lineEdit(iteration_box, self, "n_iterations", "Nr. Iterations", labelWidth=80, valueType=int, validator=QIntValidator())
        orangegui.checkBox(iteration_box, self, "is_incremental", "Incremental", callback=self.set_incremental)

        self.was_incremental = self.is_incremental

        iteration_box = gui.widgetBox(main_box, "", orientation="vertical", width=250)

        self.le_current_iteration = gui.lineEdit(iteration_box, self, "current_iteration", "Current Iteration", labelWidth=120, valueType=int, orientation="horizontal")
        self.le_current_iteration.setReadOnly(True)
        self.le_current_iteration.setStyleSheet("background-color: #FAFAB0; color: #252468")
        font = QFont(self.le_current_iteration.font())
        font.setBold(True)
        self.le_current_iteration.setFont(font)

        orangegui.separator(main_box)

        self.plot_box = gui.widgetBox(main_box, "Plotting Options", orientation="vertical", width=self.CONTROL_AREA_WIDTH-20)

        self.cb_interactive = orangegui.checkBox(self.plot_box, self, "is_interactive", "Update plots while fitting:", callback=self.set_interactive)
        orangegui.separator(self.plot_box, height=8)

        self.cb_show_wss_gof           = orangegui.checkBox(self.plot_box, self, "show_wss_gof", "W.S.S. and G.o.F." )
        self.cb_show_ipf               = orangegui.checkBox(self.plot_box, self, "show_ipf", "Instrumental Profile")
        self.cb_show_shift             = orangegui.checkBox(self.plot_box, self, "show_shift", "Calibration Shift")
        self.cb_show_size              = orangegui.checkBox(self.plot_box, self, "show_size", "Size Distribution")
        self.cb_show_warren            = orangegui.checkBox(self.plot_box, self, "show_warren", "Warren's Plot")
        self.cb_show_integral_breadth  = orangegui.checkBox(self.plot_box, self, "show_integral_breadth", "Integral Breadth")

        self.set_interactive()

        tab_free_out = gui.widgetBox(main_box, "Free Output Parameters", orientation="vertical")

        self.scrollarea_free_out = QScrollArea(tab_free_out)
        self.scrollarea_free_out.setMinimumWidth(self.CONTROL_AREA_WIDTH-55)
        self.scrollarea_free_out.setMaximumHeight(170)

        def write_text():
            self.free_output_parameters_text = self.text_area_free_out.toPlainText()

        self.text_area_free_out = gui.textArea(height=1000, width=1000, readOnly=False)
        self.text_area_free_out.setText(self.free_output_parameters_text)
        self.text_area_free_out.textChanged.connect(write_text)

        self.scrollarea_free_out.setWidget(self.text_area_free_out)
        self.scrollarea_free_out.setWidgetResizable(1)

        tab_free_out.layout().addWidget(self.scrollarea_free_out, alignment=Qt.AlignHCenter)

        self.tabs = gui.tabWidget(self.mainArea)

        self.tab_fit_in  = gui.createTabPage(self.tabs, "Fit Input Parameters")
        self.tab_plot    = gui.createTabPage(self.tabs, "Plots")
        self.tab_fit_out = gui.createTabPage(self.tabs, "Fit Output Parameters")

        self.tabs_plot = gui.tabWidget(self.tab_plot)

        self.tab_plot_fit_data         = gui.createTabPage(self.tabs_plot, "Fit")
        self.tab_plot_fit_wss          = gui.createTabPage(self.tabs_plot, "W.S.S.")
        self.tab_plot_fit_gof          = gui.createTabPage(self.tabs_plot, "G.o.F.")
        self.tab_plot_ipf              = gui.createTabPage(self.tabs_plot, "Instrumental Profile")
        self.tab_plot_size             = gui.createTabPage(self.tabs_plot, "Size Distribution")
        self.tab_plot_strain           = gui.createTabPage(self.tabs_plot, "Warren's Plot")
        self.tab_plot_integral_breadth = gui.createTabPage(self.tabs_plot, "Integral Breadth")

        self.fit_text_output = gui.textArea(height=100, width=865)

        out_box = gui.widgetBox(self.mainArea, "Fit Output", addSpace=False, orientation="horizontal")
        out_box.layout().addWidget(self.fit_text_output)

        # ---------------------------------------------------------------\

        self.tabs_plot_fit_data = gui.tabWidget(self.tab_plot_fit_data)

        self.__build_plot_fit()

        # ---------------------------------------------------------------\

        self.plot_fit_wss = PlotWindow()
        self.plot_fit_wss.setDefaultPlotLines(True)
        self.plot_fit_wss.setActiveCurveColor(color="#00008B")
        self.plot_fit_wss.setGraphXLabel("Iteration")
        self.plot_fit_wss.setGraphYLabel("WSS")

        self.tab_plot_fit_wss.layout().addWidget(self.plot_fit_wss)

        self.plot_fit_gof = PlotWindow()
        self.plot_fit_gof.setDefaultPlotLines(True)
        self.plot_fit_gof.setActiveCurveColor(color="#00008B")
        self.plot_fit_gof.setGraphXLabel("Iteration")
        self.plot_fit_gof.setGraphYLabel("GOF")

        self.tab_plot_fit_gof.layout().addWidget(self.plot_fit_gof)

        # ---------------------------------------------------------------

        self.tabs_plot_ipf      = gui.tabWidget(self.tab_plot_ipf)

        self.__build_plot_ipf()

        # ---------------------------------------------------------------

        self.tabs_plot_size = gui.tabWidget(self.tab_plot_size)

        self.__build_plot_size()

        # ---------------------------------------------------------------

        self.tabs_plot_strain = gui.tabWidget(self.tab_plot_strain)

        self.__build_plot_strain()

        # ---------------------------------------------------------------

        self.tabs_plot_integral_breadth = gui.tabWidget(self.tab_plot_integral_breadth)

        self.__build_plot_integral_breadth()

        # ---------------------------------------------------------------

        def get_box_header(widget, tab_widget):
            orangegui.separator(tab_widget)
            box_header = gui.widgetBox(tab_widget, "", orientation="horizontal", width=600)

            le = gui.lineEdit(box_header, widget, "fixed_label", "Color Codes: ", valueType=str)
            le.setStyleSheet("background-color: rgb(190,190,190);")
            le = gui.lineEdit(box_header, widget, "function_label", "fixed    ", valueType=str)
            le.setStyleSheet("background-color: rgb(169,208,245);")
            le = gui.lineEdit(box_header, widget, "free_input_parameter_label", "function    ", valueType=str)
            le.setStyleSheet("background-color: rgb(213,245,227);")
            le = gui.lineEdit(box_header, widget, "free_output_parameter_label", "free input parameter    ", valueType=str)
            le.setStyleSheet("background-color: rgb(242,245,169);")
            gui.widgetLabel(box_header, "free output parameter")
            orangegui.separator(tab_widget)

        get_box_header(self, self.tab_fit_in)
        get_box_header(self, self.tab_fit_out)

        self.table_fit_in = self.__create_table_widget(is_output=False)

        self.tab_fit_in.layout().addWidget(self.table_fit_in, alignment=Qt.AlignHCenter)

        # ---------------------------------------------------------------

        self.table_fit_out = self.__create_table_widget()

        self.tab_fit_out.layout().addWidget(self.table_fit_out, alignment=Qt.AlignHCenter)

    def fit_text_write(self, text):
        cursor = self.fit_text_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text + "\n")
        self.fit_text_output.setTextCursor(cursor)
        self.fit_text_output.ensureCursorVisible()

    def set_incremental(self):
        if self.is_incremental == 0:
            if self.was_incremental == 1:
                answer = QMessageBox.question(self, 'Set Incremental', "Unchecking incremental mode will make the fit begin from initially received parameters, continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if (answer == QMessageBox.No):
                    self.is_incremental = 1

        self.was_incremental = self.is_incremental

    def set_interactive(self):
        self.cb_show_wss_gof.setEnabled(self.is_interactive==1)

        if not self.fit_global_parameters is None:
            if self.is_interactive == 1:
                self.cb_show_ipf.setEnabled(not self.fit_global_parameters.instrumental_profile_parameters is None)
                self.cb_show_shift.setEnabled(not self.fit_global_parameters.get_shift_parameters(Lab6TanCorrection.__name__) is None)
                self.cb_show_size.setEnabled(not self.fit_global_parameters.size_parameters is None)
                self.cb_show_warren.setEnabled(not self.fit_global_parameters.strain_parameters is None)
                self.cb_show_integral_breadth.setEnabled(not (self.fit_global_parameters.strain_parameters is None and
                                                              self.fit_global_parameters.size_parameters is None and
                                                              self.fit_global_parameters.instrumental_profile_parameters is None))
            else:
                self.cb_show_ipf.setEnabled(False)
                self.cb_show_shift.setEnabled(False)
                self.cb_show_size.setEnabled(False)
                self.cb_show_warren.setEnabled(False)
                self.cb_show_integral_breadth.setEnabled(False)
        else:
            self.cb_show_ipf.setEnabled(self.is_interactive==1)
            self.cb_show_shift.setEnabled(self.is_interactive==1)
            self.cb_show_size.setEnabled(self.is_interactive==1)
            self.cb_show_warren.setEnabled(self.is_interactive==1)
            self.cb_show_integral_breadth.setEnabled(self.is_interactive==1)

    def set_plot_options_enabled(self, enabled):
        self.fit_button.setEnabled(enabled)
        self.plot_box.setEnabled(enabled)
        self.plot_box.repaint()

    #####################################
    # INPUT
    #####################################

    def set_data(self, data):
        try:
            if not data is None:
                if self.fit_running: raise RuntimeError("Fit is Running: Input data are not accepted!")

                if self.is_incremental == 1 and not self.fit_global_parameters is None:
                    if not ConfirmDialog.confirmed(self, message="Warning: Fitter is in set in incremental mode, but received fit parameters will replace the already fitted ones. Do you accept them?"):
                        return

                self.current_iteration = 0

                self.fit_global_parameters = data.duplicate()
                self.initial_fit_global_parameters = data.duplicate()

                # keep existing text!
                received_free_output_parameters = self.fit_global_parameters.free_output_parameters.duplicate()

                existing_free_output_parameters = FreeOutputParameters()
                existing_free_output_parameters.parse_formulas(self.free_output_parameters_text)
                existing_free_output_parameters.append(received_free_output_parameters) # received overwrite parameters with same name

                self.text_area_free_out.setText(existing_free_output_parameters.to_python_code())

                parameters = self.fit_global_parameters.free_input_parameters.as_parameters()
                parameters.extend(self.fit_global_parameters.get_parameters())

                self.__populate_table(self.table_fit_in, parameters, is_output=False)

                self.tabs.setCurrentIndex(0)

                if self.fit_global_parameters.instrumental_profile_parameters is None:
                    self.show_ipf = 0
                    self.cb_show_ipf.setEnabled(False)
                    self.__set_enable_ipf_tabs(False)
                else:
                    self.cb_show_ipf.setEnabled(True)
                    self.__set_enable_ipf_tabs(True)

                if self.fit_global_parameters.get_shift_parameters(Lab6TanCorrection.__name__) is None:
                    self.show_shift = 0
                    self.cb_show_shift.setEnabled(False)
                    self.__set_enabled_shift_tabs(False)
                else:
                    self.cb_show_shift.setEnabled(True)
                    self.__set_enabled_shift_tabs(True)

                if self.fit_global_parameters.size_parameters is None:
                    self.show_size = 0
                    self.cb_show_size.setEnabled(False)
                    self.tab_plot_size.setEnabled(False)
                else:
                    self.cb_show_size.setEnabled(True)
                    self.tab_plot_size.setEnabled(True)

                if self.fit_global_parameters.strain_parameters is None:
                    self.show_warren           = 0
                    self.cb_show_warren.setEnabled(False)
                    self.tab_plot_strain.setEnabled(False)
                else:
                    self.cb_show_warren.setEnabled(True)
                    self.tab_plot_strain.setEnabled(True)

                if self.fit_global_parameters.strain_parameters is None and \
                   self.fit_global_parameters.size_parameters is None and \
                   self.fit_global_parameters.instrumental_profile_parameters is None:
                    self.show_integral_breadth = 0
                    self.cb_show_integral_breadth.setEnabled(False)
                    self.tab_plot_integral_breadth.setEnabled(False)
                else:
                    self.cb_show_integral_breadth.setEnabled(True)
                    self.tab_plot_integral_breadth.setEnabled(True)

                self.set_interactive()
                self.was_incremental = self.is_incremental
                self.__initialize_fit(is_init=True)
                self.__show_data(is_init=True)

                if self.is_automatic_run:
                    self.do_fit()
        except Exception as e:
            QMessageBox.critical(self, "Error during load",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def __set_enable_ipf_tabs(self, enabled=True):
        for index in range(len(self.tabs_plot_ipf)):
            self.tab_plot_fwhm[index].setEnabled(enabled)
            self.tab_plot_eta[index].setEnabled(enabled)

    def __set_enabled_shift_tabs(self, enabled=True):
        for index in range(len(self.tabs_plot_ipf)):
            self.tab_plot_lab6[index].setEnabled(enabled)

    def __create_table_widget(self, is_output=True):
        from PyQt5.QtWidgets import QAbstractItemView

        table_fit = QTableWidget(1, 8 if is_output else 7)
        table_fit.setMinimumWidth(865)
        table_fit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        table_fit.setAlternatingRowColors(True)
        table_fit.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table_fit.verticalHeader().setVisible(False)
        table_fit.setHorizontalHeaderLabels(self.horizontal_headers if is_output else self.horizontal_headers[:-1])
        table_fit.setSelectionBehavior(QAbstractItemView.SelectRows)

        return table_fit

    def __add_table_item(self,
                         table_widget,
                         row_index,
                         column_index,
                         text="",
                         alignement=Qt.AlignLeft,
                         change_color=False,
                         color=QColor(255, 255, 255)):

            table_item = QTableWidgetItem(text)
            table_item.setTextAlignment(alignement)
            if change_color: table_item.setBackground(color)
            table_widget.setItem(row_index, column_index, table_item)

    def __populate_table(self, table_widget, parameters, is_output=True):
        table_widget.clear()

        row_count = table_widget.rowCount()
        for n in range(0, row_count):
            table_widget.removeRow(0)

        for index in range(0, len(parameters)):
            table_widget.insertRow(0)

        for index in range(0, len(parameters)):
            parameter = parameters[index]

            change_color = not parameter.is_variable()

            if change_color:
                if parameter.input_parameter: color = QColor(213, 245, 227)
                elif parameter.fixed: color = QColor(190, 190, 190)
                elif parameter.output_parameter: color = QColor(242, 245, 169)
                else: color = QColor(169, 208, 245)
            else:
                color = None

            self.__add_table_item(table_widget, index, 0,
                                  parameter.parameter_name,
                                  Qt.AlignLeft, change_color, color)

            self.__add_table_item(table_widget, index, 1,
                                  str(round(0.0 if parameter.value is None else parameter.value, 6)),
                                  Qt.AlignRight, change_color, color)

            if (not parameter.is_variable()) or parameter.boundary is None: text_2 = text_3 = ""
            else:
                if parameter.boundary.min_value == PARAM_HWMIN: text_2 = ""
                else: text_2 = str(round(0.0 if parameter.boundary.min_value is None else parameter.boundary.min_value, 6))

                if parameter.boundary.max_value == PARAM_HWMAX: text_3 = ""
                else: text_3 = str(round(0.0 if parameter.boundary.max_value is None else parameter.boundary.max_value, 6))

            self.__add_table_item(table_widget, index, 2,
                                  text_2,
                                  Qt.AlignRight, change_color, color)
            self.__add_table_item(table_widget, index, 3,
                                  text_3,
                                  Qt.AlignRight, change_color, color)

            self.__add_table_item(table_widget, index, 4,
                                "" if not parameter.fixed else "\u2713",
                                  Qt.AlignCenter, change_color, color)
            self.__add_table_item(table_widget, index, 5,
                                "" if not parameter.function else "\u2713",
                                  Qt.AlignCenter, change_color, color)

            if parameter.function: text_6 = str(parameter.function_value)
            else: text_6 = ""

            self.__add_table_item(table_widget, index, 6,
                                  text_6,
                                  Qt.AlignLeft, change_color, color)

            if is_output: self.__add_table_item(table_widget, index, 7,
                                                str(round(0.0 if parameter.error is None else parameter.error, 6)),
                                                Qt.AlignRight, change_color, color)

        table_widget.setHorizontalHeaderLabels(self.horizontal_headers)
        table_widget.resizeRowsToContents()
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

    #####################################
    # FIT
    #####################################

    def do_fit(self):
        try:
            if not self.fit_global_parameters is None:
                self.set_plot_options_enabled(False)
                self.stop_fit = False

                congruence.checkStrictlyPositiveNumber(self.n_iterations, "Nr. Iterations")

                if self.fit_global_parameters.fit_initialization is None:
                    raise ValueError("Mandatory widgets (Fit Initialization) is missing.")

                if self.fit_global_parameters.fit_initialization.fft_parameters is None:
                    raise ValueError("FFT parameters is missing: add the proper widget before the Fitter")

                if self.fit_global_parameters.measured_dataset is None:
                    raise ValueError("Mandatory widgets (Load Data/Radiation/Phases/Line Profile) are completely missing.")

                if self.fit_global_parameters.measured_dataset.diffraction_patterns is None:
                    raise ValueError("Diffraction Pattern is missing: add the proper widget before the Fitter")

                if self.fit_global_parameters.measured_dataset.phases is None:
                    raise ValueError("Phases is missing: add the proper widget before the Fitter")

                if self.fit_global_parameters.measured_dataset.incident_radiations is None:
                    raise ValueError("Radiation is missing: add the proper widget before the Fitter")

                if self.fit_global_parameters.measured_dataset.line_profiles is None:
                    raise ValueError("Line Profiles is missing: add the proper widget before the Fitter")

                self.__initialize_fit(is_init=False)

                initial_fit_global_parameters = self.fit_global_parameters.duplicate()

                if self.is_incremental == 1 and self.current_iteration > 0:
                    if len(initial_fit_global_parameters.get_parameters()) != len(self.fitter.fit_global_parameters.get_parameters()):
                        raise Exception("Incremental Fit is not possibile!\n\nParameters in the last fitting procedure are incompatible with the received ones")

                self.fitted_fit_global_parameters = initial_fit_global_parameters
                self.current_running_iteration = 0

                try:
                    self.fit_thread = FitThread(self)
                    self.fit_thread.begin.connect(self.fit_begin)
                    self.fit_thread.text_write.connect(self.fit_text_write)
                    self.fit_thread.update.connect(self.fit_update)
                    self.fit_thread.finished.connect(self.fit_completed)
                    self.fit_thread.error.connect(self.fit_error)
                    self.fit_thread.start()
                except Exception as e:
                    raise FitNotStartedException(str(e))

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            self.set_plot_options_enabled(True)

            if self.IS_DEVELOP: raise e

        self.setStatusMessage("")
        self.progressBarFinished()

    def __initialize_fit(self, is_init=False):
        if self.is_incremental==0 or is_init:
            self.fit_global_parameters = self.initial_fit_global_parameters.duplicate()
            self.current_wss = []
            self.current_gof = []
            self.current_iteration = 0
            self.fit_data = None

        if not is_init:
            self.fit_global_parameters.set_n_max_iterations(self.n_iterations)
            self.fit_global_parameters.set_convergence_reached(False)
        else:
            self.fitter = FitterFactory.create_fitter(fitter_name=self.cb_fitter.currentText())

        self.fit_global_parameters.free_output_parameters.parse_formulas(self.free_output_parameters_text)

        self.fitted_fit_global_parameters = self.fit_global_parameters.duplicate()
        self.fitted_fit_global_parameters.evaluate_functions()

        self.fitter.initialize(self.fitted_fit_global_parameters)

        self.fitted_patterns = self.fitter.build_fitted_diffraction_pattern(self.fitted_fit_global_parameters)

        self.tabs.setCurrentIndex(1)
        self.tabs_plot.setCurrentIndex(0)

    def stop_fit(self):
        if ConfirmDialog.confirmed(self, "Confirm STOP?"):
            self.stop_fit = True

    def send_current_fit(self):
        if not self.fit_global_parameters is None:
            self.fit_global_parameters.regenerate_parameters()
            self.send("Fit Global Parameters", self.fit_global_parameters.duplicate())
            self.send("Fitted Instrumental Parameters", self.fit_global_parameters.get_instrumental_parameters())

    def save_data(self):
        try:
            if hasattr(self, "fitted_patterns") and not self.fitted_patterns is None:
                file_path = QFileDialog.getSaveFileName(self, "Select File", os.path.dirname(self.save_file_name))[0]

                if not file_path is None and not file_path.strip() == "":
                    self.save_file_name=file_path

                    text = ""
                    for diffraction_pattern_index in range(len(self.fitted_patterns)):
                        fitted_pattern = self.fitted_patterns[diffraction_pattern_index]
                        diffraction_pattern = self.fit_global_parameters.measured_dataset.get_diffraction_pattern(diffraction_pattern_index)

                        text += "" if diffraction_pattern_index==0 else "\n"
                        text += "------------------------------------------------------------------------\n"
                        text +="DIFFRACTION PATTERN Nr. " + str(diffraction_pattern_index+1) + "\n\n"
                        text += "2Theta [deg], s [Å-1], Intensity, Fit, Residual\n"
                        text += "------------------------------------------------------------------------"

                        for index in range(0, fitted_pattern.diffraction_points_count()):
                            text += "\n" + str(fitted_pattern.get_diffraction_point(index).twotheta) + "  " + \
                                    str(fitted_pattern.get_diffraction_point(index).s) + " " + \
                                    str(diffraction_pattern.get_diffraction_point(index).intensity) + " " + \
                                    str(fitted_pattern.get_diffraction_point(index).intensity) + " " + \
                                    str(fitted_pattern.get_diffraction_point(index).error) + " "

                    file = open(self.save_file_name, "w")
                    file.write(text)
                    file.flush()
                    file.close()

                    QMessageBox.information(self,
                                            "Save Data",
                                            "Fitted data saved on file:\n" + self.save_file_name,
                                            QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    ##########################################
    # PLOTS
    ##########################################

    def __show_data(self, is_init=False):
        diffraction_patterns_number = self.fitted_fit_global_parameters.measured_dataset.get_diffraction_patterns_number()
        phases_number               = self.fitted_fit_global_parameters.measured_dataset.get_phases_number()

        self.__refresh_fit(diffraction_patterns_number, is_init)
        self.__refresh_fit_data()
        self.__refresh_ipf(diffraction_patterns_number, is_init)
        self.__refresh_size(phases_number, is_init)
        self.__refresh_strain(phases_number, is_init)
        self.__refresh_integral_breadth(phases_number, diffraction_patterns_number, is_init)

        self.set_interactive()

    # ------------------------------------------------------------------------

    def __refresh_fit(self, diffraction_patterns_number, is_init=False):
        if is_init:
            self.__build_plot_fit()

            self.x = numpy.full(diffraction_patterns_number, None)
            self.y = numpy.full(diffraction_patterns_number, None)

        for diffraction_pattern_index in range(diffraction_patterns_number):
            diffraction_pattern = self.fitted_fit_global_parameters.measured_dataset.get_diffraction_pattern(diffraction_pattern_index)
            fitted_pattern      = self.fitted_patterns[diffraction_pattern_index]

            nr_points = fitted_pattern.diffraction_points_count()

            yf = numpy.zeros(nr_points)
            res = numpy.zeros(nr_points)

            if is_init:
                x = numpy.zeros(nr_points)
                y = numpy.zeros(nr_points)

                i = -1
                for point, fit in zip(diffraction_pattern.diffraction_pattern, fitted_pattern.diffraction_pattern):
                    i += 1
                    x[i]   = point.twotheta
                    y[i]   = point.intensity
                    yf[i]  = fit.intensity
                    res[i] = fit.error

                self.x[diffraction_pattern_index] = x
                self.y[diffraction_pattern_index] = y
            else:
                i = -1
                for fit in fitted_pattern.diffraction_pattern:
                    i += 1
                    yf[i]  = fit.intensity
                    res[i] = fit.error

            res = -10 + (res-numpy.max(res))

            if is_init: self.plot_fit[diffraction_pattern_index].addCurve(self.x[diffraction_pattern_index], self.y[diffraction_pattern_index], legend="data", linewidth=4, color="blue")
            self.plot_fit[diffraction_pattern_index].addCurve(self.x[diffraction_pattern_index], yf, legend="fit", color="red")
            self.plot_fit[diffraction_pattern_index].addCurve(self.x[diffraction_pattern_index], res, legend="residual", color="#2D811B")

    # ------------------------------------------------------------------------

    def __refresh_fit_data(self):
        if not self.fit_data is None and self.show_wss_gof==1:
            x = numpy.arange(1, self.current_iteration + 1)

            self.plot_fit_wss.addCurve(x, self.current_wss, legend="wss", symbol='o', color="blue")
            self.plot_fit_gof.addCurve(x, self.current_gof, legend="gof", symbol='o', color="red")

    # ------------------------------------------------------------------------

    def __refresh_ipf(self, diffraction_patterns_number, is_init=False):
        if is_init: self.__build_plot_ipf()

        fit_global_parameters = self.__fit_global_parameters()

        for diffraction_pattern_index in range(self.__get_number_of_ipf_tabs(fit_global_parameters)[1]):
            instrumental_profile_parameters = fit_global_parameters.get_instrumental_profile_parameters_item(Caglioti.__name__, diffraction_pattern_index)
            if not instrumental_profile_parameters is None:
                self.refresh_caglioti_fwhm(instrumental_profile_parameters, diffraction_pattern_index)
                self.refresh_caglioti_eta(instrumental_profile_parameters, diffraction_pattern_index)

            shift_parameters = fit_global_parameters.get_shift_parameters_item(Lab6TanCorrection.__name__, diffraction_pattern_index)
            if not shift_parameters is None: self.refresh_lab6(shift_parameters, diffraction_pattern_index)

    # ------------------------------------------------------------------------

    def refresh_caglioti_fwhm(self, instrumental_profile_parameters, diffraction_pattern_index):
        if self.show_ipf==1:
            if self.fwhm_autoscale[diffraction_pattern_index] == 1:
                twotheta_fwhm = numpy.arange(0.0, 150.0, 0.5)
            else:
                twotheta_fwhm = numpy.arange(self.fwhm_xmin[diffraction_pattern_index], self.fwhm_xmax[diffraction_pattern_index], 0.5)

            y = caglioti_fwhm(instrumental_profile_parameters.U.value,
                              instrumental_profile_parameters.V.value,
                              instrumental_profile_parameters.W.value,
                              numpy.radians(0.5*twotheta_fwhm))

            self.plot_ipf_fwhm[diffraction_pattern_index].addCurve(twotheta_fwhm, y, legend="fwhm", color="blue")

            if self.fwhm_autoscale[diffraction_pattern_index] == 0 and \
                    self.fwhm_ymin[diffraction_pattern_index] < self.fwhm_ymax[diffraction_pattern_index]:
                self.plot_ipf_fwhm[diffraction_pattern_index].setGraphYLimits(ymin=self.fwhm_ymin[diffraction_pattern_index],
                                                                              ymax=self.fwhm_ymax[diffraction_pattern_index])

    # ------------------------------------------------------------------------

    def refresh_caglioti_eta(self, instrumental_profile_parameters, diffraction_pattern_index):
        if self.show_ipf==1:
            if self.eta_autoscale[diffraction_pattern_index] == 1:
                twotheta_eta = numpy.arange(0.0, 150.0, 0.5)
            else:
                twotheta_eta = numpy.arange(self.eta_xmin[diffraction_pattern_index], self.eta_xmax[diffraction_pattern_index], 0.5)

            y = caglioti_eta(instrumental_profile_parameters.a.value,
                             instrumental_profile_parameters.b.value,
                             instrumental_profile_parameters.c.value,
                             numpy.radians(0.5*twotheta_eta))

            self.plot_ipf_eta[diffraction_pattern_index].addCurve(twotheta_eta, y, legend="eta", color="blue")

            if self.eta_autoscale[diffraction_pattern_index] == 0 and \
                    self.eta_ymin[diffraction_pattern_index] < self.eta_ymax[diffraction_pattern_index]:
                self.plot_ipf_eta[diffraction_pattern_index].setGraphYLimits(ymin=self.eta_ymin[diffraction_pattern_index],
                                                                             ymax=self.eta_ymax[diffraction_pattern_index])

    # ------------------------------------------------------------------------

    def refresh_lab6(self, shift_parameters, diffraction_pattern_index):
        if self.show_shift==1:
            if self.lab6_autoscale[diffraction_pattern_index] == 1: 
                twotheta_lab6 = numpy.arange(0.0, 150.0, 0.5)
            else:                        
                twotheta_lab6 = numpy.arange(self.lab6_xmin[diffraction_pattern_index], self.lab6_xmax[diffraction_pattern_index], 0.5)

            y = delta_two_theta_lab6(shift_parameters.ax.value,
                                     shift_parameters.bx.value,
                                     shift_parameters.cx.value,
                                     shift_parameters.dx.value,
                                     shift_parameters.ex.value,
                                     numpy.radians(0.5*twotheta_lab6))

            self.plot_ipf_lab6[diffraction_pattern_index].addCurve(twotheta_lab6, y, legend="lab6", color="blue")

            if self.lab6_autoscale[diffraction_pattern_index] == 0 and \
                    self.lab6_ymin[diffraction_pattern_index] < self.lab6_ymax[diffraction_pattern_index]:
                self.plot_ipf_lab6[diffraction_pattern_index].setGraphYLimits(ymin=self.lab6_ymin[diffraction_pattern_index], ymax=self.lab6_ymax[diffraction_pattern_index])

    # ------------------------------------------------------------------------

    def __clear_text_size(self, phase_index):
        if not self.text_size[phase_index] is None: self.text_size[phase_index].remove()

    def __refresh_size(self, phases_number=0, is_init=False):
        if is_init:
            self.distributions = numpy.full(phases_number, None)
            self.text_size = numpy.full(phases_number, None)

            self.__build_plot_size()

        for phase_index in range(phases_number):
            self.__clear_text_size(phase_index)

            size_parameters = self.fitted_fit_global_parameters.get_size_parameters(phase_index)

            if not size_parameters is None and size_parameters.active and self.show_size==1:
                self.plot_size[phase_index].setEnabled(True)

                if self.size_autoscale[phase_index]==1:
                    if self.distributions[phase_index] is None: self.distributions[phase_index] = size_parameters.get_distribution(auto=True)
                    else: self.distributions[phase_index] = size_parameters.get_distribution(auto=False,
                                                                                             D_min=self.distributions[phase_index].D_min,
                                                                                             D_max=self.distributions[phase_index].D_max)
                else:
                    self.distributions[phase_index] = size_parameters.get_distribution(auto=False,
                                                                                       D_min=self.size_xmin[phase_index],
                                                                                       D_max=self.size_xmax[phase_index])
                distribution = self.distributions[phase_index]

                self.plot_size[phase_index].addCurve(distribution.x, distribution.y, legend="distribution", color="blue")
                self.text_size[phase_index] = self.plot_size[phase_index]._backend.ax.text(numpy.max(distribution.x) * 0.65, numpy.max(distribution.y) * 0.7,
                                                                                           "<D>        = " + str(round(distribution.D_avg, 3)) + " nm\n" + \
                                                                                           "<D> s.w. = " + str(round(distribution.D_avg_surface_weighted, 3)) + " nm\n" + \
                                                                                           "<D> v.w. = " + str(round(distribution.D_avg_volume_weighted, 3)) + " nm\n" + \
                                                                                           "s.d.           = " + str(round(distribution.standard_deviation, 3)) + " nm", fontsize=12)
            else:
                self.plot_size[phase_index].setEnabled(False)

    def refresh_size(self, size_parameters, phase_index):
        if self.show_size==1:
            self.__clear_text_size(phase_index)

            if self.size_autoscale[phase_index] == 1:
                if self.distributions[phase_index] is None:
                    self.distributions[phase_index] = size_parameters.get_distribution(auto=True)
                else:
                    self.distributions[phase_index] = size_parameters.get_distribution(auto=False,
                                                                                       D_min=self.distributions[phase_index].D_min,
                                                                                       D_max=self.distributions[phase_index].D_max)
            else:
                self.distributions[phase_index] = size_parameters.get_distribution(auto=False,
                                                                                   D_min=self.size_xmin[phase_index],
                                                                                   D_max=self.size_xmax[phase_index])

            distribution = self.distributions[phase_index]

            self.plot_size[phase_index].addCurve(distribution.x, distribution.y, legend="distribution", color="blue")
            self.text_size[phase_index] = self.plot_size[phase_index]._backend.ax.text(numpy.max(distribution.x) * 0.65, numpy.max(distribution.y) * 0.7,
                                                                                       "<D>        = " + str(round(distribution.D_avg, 3)) + " nm\n" + \
                                                                                       "<D> s.w. = " + str(round(distribution.D_avg_surface_weighted, 3)) + " nm\n" + \
                                                                                       "<D> v.w. = " + str(round(distribution.D_avg_volume_weighted, 3)) + " nm\n" + \
                                                                                       "s.d.           = " + str(round(distribution.standard_deviation, 3)) + " nm", fontsize=12)

    # ------------------------------------------------------------------------

    def __refresh_strain(self, phases_number=0, is_init=False):
        if is_init: self.__build_plot_strain()

        for phase_index in range(phases_number):
            strain_parameters = self.fitted_fit_global_parameters.get_strain_parameters(phase_index)

            if not strain_parameters is None and strain_parameters.active and self.show_warren==1:
                if self.distributions is None or self.distributions[phase_index] is None: L_max = 20
                else: L_max = 2*self.distributions[phase_index].D_avg

                x, y = strain_parameters.get_warren_plot(1, 0, 0, L_max=L_max)
                self.plot_strain[phase_index].addCurve(x, y, legend="h00", color='blue')
                _, y = strain_parameters.get_warren_plot(1, 1, 1, L_max=L_max)
                self.plot_strain[phase_index].addCurve(x, y, legend="hhh", color='red')
                _, y = strain_parameters.get_warren_plot(1, 1, 0, L_max=L_max)
                self.plot_strain[phase_index].addCurve(x, y, legend="hh0", color='green')

    # ------------------------------------------------------------------------

    def __clear_annotations(self, diffraction_pattern_index, phase_index):
        annotations = self.annotations_ib[diffraction_pattern_index, phase_index]
        if not annotations is None:
            for annotation in self.annotations_ib[diffraction_pattern_index, phase_index]:
                if not annotation is None: annotation.remove()

    def __refresh_integral_breadth(self, phases_number, diffraction_pattern_number, is_init=False):
        if is_init:
            self.x_ib           = numpy.full((diffraction_pattern_number, phases_number), None)
            self.labels_ib      = numpy.full((diffraction_pattern_number, phases_number), None)
            self.annotations_ib = numpy.full((diffraction_pattern_number, phases_number), None)

            self.__build_plot_integral_breadth()

        fit_global_parameters = self.__fit_global_parameters()

        if not (fit_global_parameters.strain_parameters is None and \
                fit_global_parameters.size_parameters is None and \
                fit_global_parameters.instrumental_profile_parameters is None) and \
                self.show_integral_breadth==1:
            for diffraction_pattern_index in range(self.__get_number_of_ipf_tabs(fit_global_parameters)[1]):
                line_profile       = fit_global_parameters.measured_dataset.get_line_profile(diffraction_pattern_index)
                incident_radiation = fit_global_parameters.measured_dataset.get_incident_radiations_item(diffraction_pattern_index)
                wavelength         = incident_radiation.wavelength.value

                instrumental_profile_parameters = fit_global_parameters.get_instrumental_profile_parameters_item(Caglioti.__name__, diffraction_pattern_index)

                for phase_index in range(phases_number):
                    self.__clear_annotations(diffraction_pattern_index, phase_index)

                    phase             = fit_global_parameters.measured_dataset.get_phase(phase_index)
                    lattice_parameter = phase.a.value

                    nr_points = line_profile.get_reflections_number(phase_index=phase_index)

                    self.x_ib[diffraction_pattern_index, phase_index]      = line_profile.get_s_list(phase_index)
                    self.labels_ib[diffraction_pattern_index, phase_index] = line_profile.get_hkl_list(phase_index)

                    size_parameters   = fit_global_parameters.get_size_parameters(phase_index)
                    strain_parameters = fit_global_parameters.get_strain_parameters(phase_index)

                    plot_instr = not instrumental_profile_parameters is None
                    plot_size = not size_parameters is None and size_parameters.active
                    plot_strain = not strain_parameters is None and strain_parameters.active

                    ##########################################

                    if plot_size and not size_parameters.shape == Shape.WULFF:
                        y_ib_size = numpy.full(line_profile.get_reflections_number(phase_index), integral_breadth_size(None, size_parameters))
                    else:
                        y_ib_size = numpy.zeros(nr_points)

                    y_ib_strain = numpy.zeros(nr_points)
                    y_ib_instr  = numpy.zeros(nr_points)
                    y_ib_total  = numpy.zeros(nr_points)

                    i = -1
                    for reflection in line_profile.get_reflections(phase_index):
                        i += 1

                        if plot_size and size_parameters.shape == Shape.WULFF:
                            y_ib_size[i] = integral_breadth_size(reflection, size_parameters)

                        if plot_strain:
                            y_ib_strain[i] = integral_breadth_strain(reflection,
                                                                     lattice_parameter,
                                                                     strain_parameters)

                        if plot_instr:
                            y_ib_instr[i] = integral_breadth_instrumental_function(reflection,
                                                                                   lattice_parameter,
                                                                                   wavelength,
                                                                                   instrumental_profile_parameters)

                        y_ib_total[i] = integral_breadth_total(reflection,
                                                               lattice_parameter,
                                                               wavelength,
                                                               instrumental_profile_parameters,
                                                               size_parameters,
                                                               strain_parameters)

                    x_ib = self.x_ib[diffraction_pattern_index, phase_index]

                    if plot_instr:  self.plot_integral_breadth[diffraction_pattern_index][phase_index].addCurve(x_ib, y_ib_instr, legend="IPF", symbol='o', color="black")
                    if plot_size:   self.plot_integral_breadth[diffraction_pattern_index][phase_index].addCurve(x_ib, y_ib_size, legend="Size", symbol='o', color="red")
                    if plot_strain: self.plot_integral_breadth[diffraction_pattern_index][phase_index].addCurve(x_ib, y_ib_strain, legend="Strain", symbol='o', color="blue")

                    y_ib_total[numpy.where(numpy.logical_or(numpy.isinf(y_ib_total), numpy.isnan(y_ib_total)))] = 0.0

                    self.plot_integral_breadth[diffraction_pattern_index][phase_index].addCurve(x_ib, y_ib_total, legend="Total", symbol='o', color="#2D811B")
                    self.plot_integral_breadth[diffraction_pattern_index][phase_index].setGraphYLimits(-0.05, numpy.max(y_ib_total)*1.2)
                    self.plot_integral_breadth[diffraction_pattern_index][phase_index].setGraphXLimits(x_ib[0] - abs(x_ib[0])*0.1, x_ib[-1] + abs(x_ib[0])*0.1)

                    ax     = self.plot_integral_breadth[diffraction_pattern_index][phase_index]._backend.ax
                    labels = self.labels_ib[diffraction_pattern_index, phase_index]
                    dy     = (numpy.max(y_ib_total)-numpy.min(y_ib_instr))*0.125

                    self.annotations_ib[diffraction_pattern_index, phase_index] = [ax.annotate(hkl, (x_ib[i], y_ib_total[i] + dy), rotation=90) for i, hkl in enumerate(labels)]

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    def __fit_global_parameters(self):
        return self.fit_global_parameters if self.fitted_fit_global_parameters is None else self.fitted_fit_global_parameters

    def __diffraction_patterns_range(self, fit_global_parameter):
        return 1 if fit_global_parameter is None else fit_global_parameter.measured_dataset.get_diffraction_patterns_number()

    def __phases_range(self, fit_global_parameter):
        return 1 if fit_global_parameter is None else fit_global_parameter.measured_dataset.get_phases_number()

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------

    def __get_number_of_ipf_tabs(self, fit_global_parameters):
        if fit_global_parameters is None: return False, 1
        else:
            caglioti_list = fit_global_parameters.get_instrumental_profile_parameters(Caglioti.__name__)
            shift_list    = fit_global_parameters.get_shift_parameters(Lab6TanCorrection.__name__)

            if not caglioti_list is None:
                ipf_number = len(caglioti_list)
            elif not shift_list is None:
                ipf_number = len(shift_list)
            else:
                ipf_number = 0

            use_single_set = (ipf_number == 1 and fit_global_parameters.measured_dataset.get_diffraction_patterns_number() > 1)

            if use_single_set: return True, 1
            else: return False, self.__diffraction_patterns_range(fit_global_parameters)

    def __build_plot_fit(self):
        fit_global_parameters = self.__fit_global_parameters()

        self.plot_fit = []
        self.tabs_plot_fit_data.clear()

        for diffraction_pattern_index in range(self.__diffraction_patterns_range(fit_global_parameters)):
            tab_plot_fit_data = gui.createTabPage(self.tabs_plot_fit_data, OWGenericWidget.diffraction_pattern_name(fit_global_parameters, diffraction_pattern_index))

            plot_fit = PlotWindow()
            plot_fit.setDefaultPlotLines(True)
            plot_fit.setActiveCurveColor(color="#00008B")
            plot_fit.setGraphXLabel(r"2$\theta$ (deg)")
            plot_fit.setGraphYLabel("Intensity")

            self.plot_fit.append(plot_fit)
            tab_plot_fit_data.layout().addWidget(plot_fit)

    def __build_plot_ipf(self):
        fit_global_parameters = self.__fit_global_parameters()

        self.plot_ipf_fwhm = []
        self.plot_ipf_eta = []
        self.plot_ipf_lab6 =[]
        self.tab_plot_fwhm = []
        self.tab_plot_eta  = []
        self.tab_plot_lab6 = []
        self.fwhm_box_array = []
        self.eta_box_array  = []
        self.lab6_box_array = []


        self.tabs_plot_ipf.clear()

        use_single_set, number_of_ipf_tabs = self.__get_number_of_ipf_tabs(fit_global_parameters)

        for diffraction_pattern_index in range(number_of_ipf_tabs):
            tab_plot_ipf = gui.tabWidget(gui.createTabPage(self.tabs_plot_ipf, OWGenericWidget.diffraction_pattern_name(fit_global_parameters, diffraction_pattern_index, use_single_set)))

            tab_plot_fwhm = gui.createTabPage(tab_plot_ipf, "Caglioti's FWHM")
            tab_plot_eta  = gui.createTabPage(tab_plot_ipf, "Caglioti's \u03b7")
            tab_plot_lab6 = gui.createTabPage(tab_plot_ipf, "LaB6 Tan Correction")

            if diffraction_pattern_index < len(self.fwhm_autoscale):
                self.fwhm_box_array.append(FWHMBox(widget=self,
                                                   parent=tab_plot_fwhm,
                                                   fit_global_parameters=fit_global_parameters,
                                                   diffraction_pattern_index=diffraction_pattern_index,
                                                   fwhm_autoscale=self.fwhm_autoscale[diffraction_pattern_index],
                                                   fwhm_xmin=self.fwhm_xmin[diffraction_pattern_index],
                                                   fwhm_xmax=self.fwhm_xmax[diffraction_pattern_index],
                                                   fwhm_ymin=self.fwhm_ymin[diffraction_pattern_index],
                                                   fwhm_ymax=self.fwhm_ymax[diffraction_pattern_index]))
            else:
                self.fwhm_box_array.append(FWHMBox(widget=self,
                                                   parent=tab_plot_fwhm,
                                                   fit_global_parameters=fit_global_parameters,
                                                   diffraction_pattern_index=diffraction_pattern_index))

            if diffraction_pattern_index < len(self.eta_autoscale):
                self.eta_box_array.append(EtaBox(widget=self,
                                                 parent=tab_plot_eta,
                                                 fit_global_parameters=fit_global_parameters,
                                                 diffraction_pattern_index=diffraction_pattern_index,
                                                 eta_autoscale=self.eta_autoscale[diffraction_pattern_index],
                                                 eta_xmin=self.eta_xmin[diffraction_pattern_index],
                                                 eta_xmax=self.eta_xmax[diffraction_pattern_index],
                                                 eta_ymin=self.eta_ymin[diffraction_pattern_index],
                                                 eta_ymax=self.eta_ymax[diffraction_pattern_index]))
            else:
                self.eta_box_array.append(EtaBox(widget=self,
                                                 parent=tab_plot_eta,
                                                 fit_global_parameters=fit_global_parameters,
                                                 diffraction_pattern_index=diffraction_pattern_index))

            if diffraction_pattern_index < len(self.lab6_autoscale):
                self.lab6_box_array.append(Lab6Box(widget=self,
                                                   parent=tab_plot_lab6,
                                                   fit_global_parameters=fit_global_parameters,
                                                   diffraction_pattern_index=diffraction_pattern_index,
                                                   lab6_autoscale=self.lab6_autoscale[diffraction_pattern_index],
                                                   lab6_xmin=self.lab6_xmin[diffraction_pattern_index],
                                                   lab6_xmax=self.lab6_xmax[diffraction_pattern_index],
                                                   lab6_ymin=self.lab6_ymin[diffraction_pattern_index],
                                                   lab6_ymax=self.lab6_ymax[diffraction_pattern_index]))
            else:
                self.lab6_box_array.append(Lab6Box(widget=self,
                                                   parent=tab_plot_lab6,
                                                   fit_global_parameters=fit_global_parameters,
                                                   diffraction_pattern_index=diffraction_pattern_index))


            self.tab_plot_fwhm.append(tab_plot_fwhm)
            self.tab_plot_eta.append(tab_plot_eta)
            self.tab_plot_lab6.append(tab_plot_lab6)

        self.dump_ipf()

    # ------------------------------------------------------------------------

    def __build_plot_size(self):
        fit_global_parameters = self.__fit_global_parameters()

        self.plot_size = []
        self.size_box_array = []

        self.tabs_plot_size.clear()

        for phase_index in range(self.__phases_range(fit_global_parameters)):
            tab_plot_size = gui.createTabPage(self.tabs_plot_size, OWGenericWidget.phase_name(fit_global_parameters, phase_index))

            if phase_index < len(self.size_autoscale):
                self.size_box_array.append(SizeBox(widget=self,
                                                   parent=tab_plot_size,
                                                   fit_global_parameters=fit_global_parameters,
                                                   phase_index=phase_index,
                                                   size_autoscale=self.size_autoscale[phase_index],
                                                   size_xmin=self.size_xmin[phase_index],
                                                   size_xmax=self.size_xmax[phase_index]))
            else:
                self.size_box_array.append(SizeBox(widget=self,
                                                   parent=tab_plot_size,
                                                   fit_global_parameters=fit_global_parameters,
                                                   phase_index=phase_index))

        self.dump_size()

    # ------------------------------------------------------------------------

    def __build_plot_strain(self):
        fit_global_parameter = self.__fit_global_parameters()

        self.plot_strain = []
        self.tabs_plot_strain.clear()

        for phase_index in range(self.__phases_range(fit_global_parameter)):
            tab_plot_strain = gui.createTabPage(self.tabs_plot_strain, OWGenericWidget.phase_name(fit_global_parameter, phase_index))

            plot_strain = PlotWindow(control=True)
            legends_dock_widget = LegendsDockWidget(plot=plot_strain)
            plot_strain._legendsDockWidget = legends_dock_widget
            plot_strain._dockWidgets.append(legends_dock_widget)
            plot_strain.addDockWidget(qt.Qt.RightDockWidgetArea, legends_dock_widget)
            plot_strain._legendsDockWidget.setFixedWidth(120)
            plot_strain.getLegendsDockWidget().show()

            plot_strain.setDefaultPlotLines(True)
            plot_strain.setActiveCurveColor(color="#00008B")
            plot_strain.setGraphTitle("Warren's plot")
            plot_strain.setGraphXLabel(r"L [nm]")
            plot_strain.setGraphYLabel("$\sqrt{<{\Delta}L^{2}>}$ [nm]")

            self.plot_strain.append(plot_strain)
            tab_plot_strain.layout().addWidget(plot_strain)

    # ------------------------------------------------------------------------

    def __build_plot_integral_breadth(self):
        fit_global_parameters = self.__fit_global_parameters()

        self.plot_integral_breadth = []
        self.tabs_plot_integral_breadth.clear()

        use_single_set, number_of_ipf_tabs = self.__get_number_of_ipf_tabs(fit_global_parameters)

        for diffraction_pattern_index in range(number_of_ipf_tabs):
            tab_plot_integral_breadth = gui.createTabPage(self.tabs_plot_integral_breadth, OWGenericWidget.diffraction_pattern_name(fit_global_parameters, diffraction_pattern_index, use_single_set))

            tabs_plot_integral_breadth_phases = gui.tabWidget(tab_plot_integral_breadth)
            plot_integral_breadth_phases = []

            for phase_index in range(self.__phases_range(fit_global_parameters)):
                tab_plot_integral_breadth_phase = gui.createTabPage(tabs_plot_integral_breadth_phases, OWGenericWidget.phase_name(fit_global_parameters, phase_index))

                plot_integral_breadth = PlotWindow(control=True)
                legends_dock_widget = LegendsDockWidget(plot=plot_integral_breadth)
                plot_integral_breadth._legendsDockWidget = legends_dock_widget
                plot_integral_breadth._dockWidgets.append(legends_dock_widget)
                plot_integral_breadth.addDockWidget(qt.Qt.RightDockWidgetArea, legends_dock_widget)
                plot_integral_breadth._legendsDockWidget.setFixedWidth(130)
                plot_integral_breadth.getLegendsDockWidget().show()

                plot_integral_breadth.setDefaultPlotLines(True)
                plot_integral_breadth.setDefaultPlotPoints(True)
                plot_integral_breadth.setActiveCurveColor(color="#00008B")
                plot_integral_breadth.setGraphTitle("Integral Breadth plot")
                plot_integral_breadth.setGraphXLabel(r"s [$nm^{-1}$]")
                plot_integral_breadth.setGraphYLabel("${\\beta}(s)$ [$nm^{-1}$]")

                tab_plot_integral_breadth_phase.layout().addWidget(plot_integral_breadth)
                plot_integral_breadth_phases.append(plot_integral_breadth)

            self.plot_integral_breadth.append(plot_integral_breadth_phases)

    ##########################################
    # THREADING
    ##########################################

    def fit_begin(self):
        #self.fit_thread.mutex.tryLock()

        self.progressBarInit()
        self.setStatusMessage("Fitting procedure started")
        self.fit_text_write("Fitting procedure started")
        self.fit_running = True

    def fit_update(self):
        try:
            self.current_iteration += 1
            self.current_running_iteration += 1

            self.progressBarSet(int(self.current_running_iteration*100/self.n_iterations))
            self.setStatusMessage("Fit iteration nr. " + str(self.current_iteration) + "/" + str(self.n_iterations) + " completed")

            if self.is_interactive == 1:
                self.__show_data()

                parameters = self.fitted_fit_global_parameters.free_input_parameters.as_parameters()
                parameters.extend(self.fitted_fit_global_parameters.get_parameters())
                parameters.extend(self.fitted_fit_global_parameters.free_output_parameters.as_parameters())

                self.__populate_table(self.table_fit_out, parameters)
        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 str(e),
                                 QMessageBox.Ok)

            if self.IS_DEVELOP: raise e

    def fit_completed(self):
        self.setStatusMessage("Fitting procedure completed")
        self.fit_text_write("Fitting procedure completed")

        self.fitted_fit_global_parameters.regenerate_parameters()

        self.fit_global_parameters = self.fitted_fit_global_parameters.duplicate()

        if self.is_incremental == 1:
            parameters = self.fit_global_parameters.free_input_parameters.as_parameters()
            parameters.extend(self.fit_global_parameters.get_parameters())

            self.__populate_table(self.table_fit_in, parameters, is_output=False)

        if self.is_interactive == 0:
            self.__show_data()

            parameters = self.fitted_fit_global_parameters.free_input_parameters.as_parameters()
            parameters.extend(self.fitted_fit_global_parameters.get_parameters())
            parameters.extend(self.fitted_fit_global_parameters.free_output_parameters.as_parameters())

            self.__populate_table(self.table_fit_out, parameters)

        self.send("Fit Global Parameters", self.fitted_fit_global_parameters)
        self.send("Fitted Instrumental Parameters", self.fitted_fit_global_parameters.get_instrumental_parameters())

        self.fit_button.setEnabled(True)
        self.set_plot_options_enabled(True)
        self.fit_running = False
        self.stop_fit = False
        self.progressBarFinished()

    def fit_error(self):
        QMessageBox.critical(self, "Error",
                             "Fit Failed: " + str(self.thread_exception),
                             QMessageBox.Ok)

        self.fit_completed()

        if self.IS_DEVELOP: raise self.thread_exception

    def dumpSettings(self):
        self.dump_ipf()
        self.dump_size()

    def dump_size(self):
        self.dump_size_autoscale()
        self.dump_size_xmin()
        self.dump_size_xmax()

    def dump_ipf(self):
        self.dump_fwhm_autoscale()
        self.dump_fwhm_xmin()
        self.dump_fwhm_xmax()
        self.dump_fwhm_ymin()
        self.dump_fwhm_ymax()

        self.dump_eta_autoscale()
        self.dump_eta_xmin()
        self.dump_eta_xmax()
        self.dump_eta_ymin()
        self.dump_eta_ymax()

        self.dump_lab6_autoscale()
        self.dump_lab6_xmin()
        self.dump_lab6_xmax()
        self.dump_lab6_ymin()
        self.dump_lab6_ymax()

    def get_parameter_box_array_fwhm(self):
        return self.fwhm_box_array

    def get_parameter_box_array_eta(self):
        return self.eta_box_array

    def get_parameter_box_array_lab6(self):
        return self.lab6_box_array

    def get_parameter_box_array_size(self):
        return self.size_box_array

    def dump_fwhm_variable(self, variable_name):
        self.get_parameter_box_array = self.get_parameter_box_array_fwhm
        self.dump_variable(variable_name)

    def dump_eta_variable(self, variable_name):
        self.get_parameter_box_array = self.get_parameter_box_array_eta
        self.dump_variable(variable_name)

    def dump_lab6_variable(self, variable_name):
        self.get_parameter_box_array = self.get_parameter_box_array_lab6
        self.dump_variable(variable_name)

    def dump_size_variable(self, variable_name):
        self.get_parameter_box_array = self.get_parameter_box_array_size
        self.dump_variable(variable_name)

    def dump_fwhm_autoscale(self): self.dump_fwhm_variable("fwhm_autoscale")
    def dump_fwhm_xmin(self): self.dump_fwhm_variable("fwhm_xmin")
    def dump_fwhm_xmax(self): self.dump_fwhm_variable("fwhm_xmax")
    def dump_fwhm_ymin(self): self.dump_fwhm_variable("fwhm_ymin")
    def dump_fwhm_ymax(self): self.dump_fwhm_variable("fwhm_ymax")

    def dump_eta_autoscale(self): self.dump_eta_variable("eta_autoscale")
    def dump_eta_xmin(self): self.dump_eta_variable("eta_xmin")
    def dump_eta_xmax(self): self.dump_eta_variable("eta_xmax")
    def dump_eta_ymin(self): self.dump_eta_variable("eta_ymin")
    def dump_eta_ymax(self): self.dump_eta_variable("eta_ymax")

    def dump_lab6_autoscale(self): self.dump_lab6_variable("lab6_autoscale")
    def dump_lab6_xmin(self): self.dump_lab6_variable("lab6_xmin")
    def dump_lab6_xmax(self): self.dump_lab6_variable("lab6_xmax")
    def dump_lab6_ymin(self): self.dump_lab6_variable("lab6_ymin")
    def dump_lab6_ymax(self): self.dump_lab6_variable("lab6_ymax")

    def dump_size_autoscale(self): self.dump_size_variable("size_autoscale")
    def dump_size_xmin(self): self.dump_size_variable("size_xmin")
    def dump_size_xmax(self): self.dump_size_variable("size_xmax")

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QVBoxLayout
from orangecontrib.wonder.util.gui_utility import InnerBox

class FWHMBox(InnerBox):
    is_on_init = True

    def __init__(self,
                 widget=None,
                 parent=None,
                 fit_global_parameters = None,
                 diffraction_pattern_index=0,
                 fwhm_autoscale=1,
                 fwhm_xmin=0.0,
                 fwhm_xmax=150.0,
                 fwhm_ymin=0.0,
                 fwhm_ymax=1.0):
        super(FWHMBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.fwhm_autoscale = fwhm_autoscale
        self.fwhm_xmin = fwhm_xmin
        self.fwhm_xmax = fwhm_xmax
        self.fwhm_ymin = fwhm_ymin
        self.fwhm_ymax = fwhm_ymax

        parent.layout().addWidget(self)
        container = self

        box = gui.widgetBox(container, "", orientation="horizontal")

        boxl = gui.widgetBox(box, "", orientation="vertical")
        boxr = gui.widgetBox(box, "", orientation="vertical", width=150)

        def set_fwhm_autoscale():
            self.le_fwhm_xmin.setEnabled(self.fwhm_autoscale==0)
            self.le_fwhm_xmax.setEnabled(self.fwhm_autoscale==0)
            self.le_fwhm_ymin.setEnabled(self.fwhm_autoscale==0)
            self.le_fwhm_ymax.setEnabled(self.fwhm_autoscale==0)
            
            if not self.is_on_init: widget.dump_fwhm_autoscale()

        orangegui.checkBox(boxr, self, "fwhm_autoscale", "Autoscale", callback=set_fwhm_autoscale)

        def refresh_caglioti_fwhm():
            if not fit_global_parameters is None:
                instrumental_profile_parameters = fit_global_parameters.get_instrumental_profile_parameters_item(Caglioti.__name__, diffraction_pattern_index)
                if not instrumental_profile_parameters is None: widget.refresh_caglioti_fwhm(instrumental_profile_parameters, diffraction_pattern_index)

        self.le_fwhm_xmin = gui.lineEdit(boxr, self, "fwhm_xmin", "2\u03b8 min", labelWidth=70, valueType=float, callback=widget.dump_fwhm_xmin)
        self.le_fwhm_xmax = gui.lineEdit(boxr, self, "fwhm_xmax", "2\u03b8 max", labelWidth=70, valueType=float, callback=widget.dump_fwhm_xmax)
        self.le_fwhm_ymin = gui.lineEdit(boxr, self, "fwhm_ymin", "FWHM min", labelWidth=70, valueType=float, callback=widget.dump_fwhm_ymin)
        self.le_fwhm_ymax = gui.lineEdit(boxr, self, "fwhm_ymax", "FWHM max", labelWidth=70, valueType=float, callback=widget.dump_fwhm_ymax)
        gui.button(boxr, self, "Refresh", height=40, callback=refresh_caglioti_fwhm)

        set_fwhm_autoscale()

        plot_ipf_fwhm = PlotWindow()
        plot_ipf_fwhm.setDefaultPlotLines(True)
        plot_ipf_fwhm.setActiveCurveColor(color="#00008B")
        plot_ipf_fwhm.setGraphXLabel("2\u03b8 (deg)")
        plot_ipf_fwhm.setGraphYLabel("FWHM (deg)")

        boxl.layout().addWidget(plot_ipf_fwhm)
        widget.plot_ipf_fwhm.append(plot_ipf_fwhm)

        self.is_on_init = False

class EtaBox(InnerBox):
    is_on_init = True

    def __init__(self,
                 widget=None,
                 parent=None,
                 fit_global_parameters=None,
                 diffraction_pattern_index=0,
                 eta_autoscale=1,
                 eta_xmin=0.0,
                 eta_xmax=150.0,
                 eta_ymin=0.0,
                 eta_ymax=1.0):
        super(EtaBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.eta_autoscale = eta_autoscale
        self.eta_xmin = eta_xmin
        self.eta_xmax = eta_xmax
        self.eta_ymin = eta_ymin
        self.eta_ymax = eta_ymax

        parent.layout().addWidget(self)
        container = self

        box = gui.widgetBox(container, "", orientation="horizontal")

        boxl = gui.widgetBox(box, "", orientation="vertical")
        boxr = gui.widgetBox(box, "", orientation="vertical", width=150)

        def set_eta_autoscale():
            self.le_eta_xmin.setEnabled(self.eta_autoscale == 0)
            self.le_eta_xmax.setEnabled(self.eta_autoscale == 0)
            self.le_eta_ymin.setEnabled(self.eta_autoscale == 0)
            self.le_eta_ymax.setEnabled(self.eta_autoscale == 0)

            if not self.is_on_init: widget.dump_eta_autoscale()

        orangegui.checkBox(boxr, self, "eta_autoscale", "Autoscale", callback=set_eta_autoscale)

        def refresh_caglioti_eta():
            if not fit_global_parameters is None:
                instrumental_profile_parameters = fit_global_parameters.get_instrumental_profile_parameters_item(Caglioti.__name__, diffraction_pattern_index)
                if not instrumental_profile_parameters is None: widget.refresh_caglioti_eta(instrumental_profile_parameters, diffraction_pattern_index)

        self.le_eta_xmin = gui.lineEdit(boxr, self, "eta_xmin", "2\u03b8 min", labelWidth=70, valueType=float, callback=widget.dump_eta_xmin)
        self.le_eta_xmax = gui.lineEdit(boxr, self, "eta_xmax", "2\u03b8 max", labelWidth=70, valueType=float, callback=widget.dump_eta_xmax)
        self.le_eta_ymin = gui.lineEdit(boxr, self, "eta_ymin", "FWHM min", labelWidth=70, valueType=float, callback=widget.dump_eta_ymin)
        self.le_eta_ymax = gui.lineEdit(boxr, self, "eta_ymax", "FWHM max", labelWidth=70, valueType=float, callback=widget.dump_eta_ymax)
        gui.button(boxr, self, "Refresh", height=40, callback=refresh_caglioti_eta)

        set_eta_autoscale()

        plot_ipf_eta = PlotWindow()
        plot_ipf_eta.setDefaultPlotLines(True)
        plot_ipf_eta.setActiveCurveColor(color="#00008B")
        plot_ipf_eta.setGraphXLabel("2\u03b8 (deg)")
        plot_ipf_eta.setGraphYLabel("FWHM (deg)")

        boxl.layout().addWidget(plot_ipf_eta)
        widget.plot_ipf_eta.append(plot_ipf_eta)

        self.is_on_init = False

class Lab6Box(InnerBox):
    is_on_init = True

    def __init__(self,
                 widget=None,
                 parent=None,
                 fit_global_parameters=None,
                 diffraction_pattern_index=0,
                 lab6_autoscale=1,
                 lab6_xmin=0.0,
                 lab6_xmax=150.0,
                 lab6_ymin=0.0,
                 lab6_ymax=1.0):
        super(Lab6Box, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.lab6_autoscale = lab6_autoscale
        self.lab6_xmin = lab6_xmin
        self.lab6_xmax = lab6_xmax
        self.lab6_ymin = lab6_ymin
        self.lab6_ymax = lab6_ymax

        parent.layout().addWidget(self)
        container = self

        box = gui.widgetBox(container, "", orientation="horizontal")

        boxl = gui.widgetBox(box, "", orientation="vertical")
        boxr = gui.widgetBox(box, "", orientation="vertical", width=150)

        def set_lab6_autoscale():
            self.le_lab6_xmin.setEnabled(self.lab6_autoscale == 0)
            self.le_lab6_xmax.setEnabled(self.lab6_autoscale == 0)
            self.le_lab6_ymin.setEnabled(self.lab6_autoscale == 0)
            self.le_lab6_ymax.setEnabled(self.lab6_autoscale == 0)

            if not self.is_on_init: widget.dump_lab6_autoscale()

        orangegui.checkBox(boxr, self, "lab6_autoscale", "Autoscale", callback=set_lab6_autoscale)

        def refresh_lab6():
            if not fit_global_parameters is None:
                shift_parameters = fit_global_parameters.get_shift_parameters_item(Lab6TanCorrection.__name__, diffraction_pattern_index)
                if not shift_parameters is None: widget.refresh_lab6(shift_parameters, diffraction_pattern_index)

        self.le_lab6_xmin = gui.lineEdit(boxr, self, "lab6_xmin", "2\u03b8 min", labelWidth=70, valueType=float, callback=widget.dump_lab6_xmin)
        self.le_lab6_xmax = gui.lineEdit(boxr, self, "lab6_xmax", "2\u03b8 max", labelWidth=70, valueType=float, callback=widget.dump_lab6_xmax)
        self.le_lab6_ymin = gui.lineEdit(boxr, self, "lab6_ymin", "FWHM min", labelWidth=70, valueType=float, callback=widget.dump_lab6_ymin)
        self.le_lab6_ymax = gui.lineEdit(boxr, self, "lab6_ymax", "FWHM max", labelWidth=70, valueType=float, callback=widget.dump_lab6_ymax)
        gui.button(boxr, self, "Refresh", height=40, callback=refresh_lab6)

        set_lab6_autoscale()

        plot_ipf_lab6 = PlotWindow()
        plot_ipf_lab6.setDefaultPlotLines(True)
        plot_ipf_lab6.setActiveCurveColor(color="#00008B")
        plot_ipf_lab6.setGraphXLabel("2\u03b8 (deg)")
        plot_ipf_lab6.setGraphYLabel("FWHM (deg)")

        boxl.layout().addWidget(plot_ipf_lab6)
        widget.plot_ipf_lab6.append(plot_ipf_lab6)

        self.is_on_init = False


class SizeBox(InnerBox):
    is_on_init = True

    def __init__(self,
                 widget=None,
                 parent=None,
                 fit_global_parameters=None,
                 phase_index=0,
                 size_autoscale=1,
                 size_xmin=0.0,
                 size_xmax=150.0):
        super(SizeBox, self).__init__()

        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)

        self.size_autoscale = size_autoscale
        self.size_xmin = size_xmin
        self.size_xmax = size_xmax

        parent.layout().addWidget(self)
        container = self

        box = gui.widgetBox(container, "", orientation="horizontal")

        boxl = gui.widgetBox(box, "", orientation="vertical")
        boxr = gui.widgetBox(box, "", orientation="vertical", width=150)

        def set_size_autoscale():
            self.le_size_xmin.setEnabled(self.size_autoscale == 0)
            self.le_size_xmax.setEnabled(self.size_autoscale == 0)

            if not self.is_on_init: widget.dump_size_autoscale()

        orangegui.checkBox(boxr, self, "size_autoscale", "Autoscale", callback=set_size_autoscale)

        def refresh_size():
            if not fit_global_parameters is None:
                size_parameters = fit_global_parameters.get_size_parameters(phase_index)
                if not size_parameters is None and size_parameters.active: widget.refresh_size(size_parameters, phase_index)

        self.le_size_xmin = gui.lineEdit(boxr, self, "size_xmin", "D min", labelWidth=70, valueType=float, callback=widget.dump_size_xmin)
        self.le_size_xmax = gui.lineEdit(boxr, self, "size_xmax", "D max", labelWidth=70, valueType=float, callback=widget.dump_size_xmax)
        gui.button(boxr, self, "Refresh", height=40, callback=refresh_size)

        set_size_autoscale()

        plot_size = PlotWindow()
        plot_size.setDefaultPlotLines(True)
        plot_size.setActiveCurveColor(color="#00008B")
        plot_size.setGraphTitle("Crystalline Domains Size Distribution")
        plot_size.setGraphXLabel(r"D [nm]")
        plot_size.setGraphYLabel("Frequency")

        widget.plot_size.append(plot_size)
        boxl.layout().layout().addWidget(plot_size)

        self.is_on_init = False
# ------------------------------------------------------------------------

import time
from PyQt5.QtCore import QThread, QMutex, pyqtSignal

class FitThread(QThread, FeedbackManager):

    begin = pyqtSignal()
    update = pyqtSignal()
    error = pyqtSignal()
    text_write = pyqtSignal(str)
    mutex = QMutex()

    def __init__(self, fitter_widget):
        super(FitThread, self).__init__(fitter_widget)
        self.fitter_widget = fitter_widget

    def run(self):
        try:
            self.mutex.lock()

            self.fitter_widget.fitter.set_feedback_manager(self)

            self.begin.emit()

            t0 = time.clock()

            for iteration in range(1, self.fitter_widget.n_iterations + 1):
                if self.fitter_widget.stop_fit: break

                self.fitter_widget.fitted_patterns, \
                self.fitter_widget.fitted_fit_global_parameters, \
                self.fitter_widget.fit_data = \
                    self.fitter_widget.fitter.do_fit(current_fit_global_parameters=self.fitter_widget.fitted_fit_global_parameters,
                                                     current_iteration=iteration,
                                                     compute_pattern=self.fitter_widget.is_interactive==1 or iteration==self.fitter_widget.n_iterations,
                                                     compute_errors=self.fitter_widget.is_interactive==1 or iteration==self.fitter_widget.n_iterations)

                self.fitter_widget.current_wss.append(self.fitter_widget.fit_data.wss)
                self.fitter_widget.current_gof.append(self.fitter_widget.fit_data.gof())

                self.feedback("Fit iteration nr. " + str(iteration) + "/" + str(self.fitter_widget.n_iterations) + " completed")

                self.update.emit()

                if self.fitter_widget.stop_fit:
                    if self.fitter_widget.is_interactive==0 and iteration<self.fitter_widget.n_iterations:
                        self.fitter_widget.fitted_patterns = \
                            self.fitter_widget.fitter.build_fitted_diffraction_pattern(fit_global_parameters=self.fitter_widget.fitted_fit_global_parameters)

                    break
                if self.fitter_widget.fitted_fit_global_parameters.is_convergence_reached(): break

            self.feedback("Fit duration: " + str(round(time.clock()-t0, 3)) + " seconds")

            self.mutex.unlock()
        except Exception as exception:
            self.mutex.unlock()

            self.fitter_widget.thread_exception = exception
            self.error.emit()

    def feedback(self, text):
        self.text_write.emit(text)

class FitNotStartedException(Exception):
    def __init__(self, *args, **kwargs): # real signature unknown
        super(FitNotStartedException, self).__init__(args, kwargs)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    ow = OWFitter()
    ow.show()
    a.exec_()
    ow.saveSettings()
