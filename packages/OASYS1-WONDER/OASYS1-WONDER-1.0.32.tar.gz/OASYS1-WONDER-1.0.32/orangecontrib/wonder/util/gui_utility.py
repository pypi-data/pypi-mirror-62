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

import os, sys

from PyQt5.QtCore import Qt, QCoreApplication, QObject, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QMessageBox, \
    QLabel, QComboBox, QTextEdit, QPushButton, QDialog, \
    QScrollArea, QDialogButtonBox

from orangewidget import gui as orangegui

OW_IS_DEVELOP = False if not "OASYSDEVELOP" in os.environ.keys() else str(os.environ.get('OASYSDEVELOP')) == "1"

current_module = sys.modules[__name__]
gui_point_size=12

class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class gui:

    @classmethod
    def button(cls, widget, master, label, callback=None, width=None, height=None,
           toggleButton=False, value="", default=False, autoDefault=True,
           buttonType=QPushButton, **misc):

        button = orangegui.button(widget, master, label, callback=callback, width=width, height=height,
                                   toggleButton=toggleButton, value=value, default=default, autoDefault=autoDefault,
                                   buttonType=buttonType, **misc)

        button.setStyleSheet("color: black;")

        return button

    # ----------------------------------
    # Default fonts
    @classmethod
    def widgetLabel(cls, widget, label="", labelWidth=None, **misc):
        lbl = QLabel(label, widget)
        if labelWidth:
            lbl.setFixedSize(labelWidth, lbl.sizeHint().height())
        orangegui.miscellanea(lbl, None, widget, **misc)

        font = lbl.font()
        font.setPointSize(current_module.gui_point_size)
        lbl.setFont(font)

        return lbl

    @classmethod
    def set_font_size(cls, point_size=12):
        current_module.gui_point_size = point_size

        qapp = QCoreApplication.instance()

        # change application font
        font = qapp.font()
        font.setPointSize(current_module.gui_point_size)
        qapp.setFont(font)

        # change orange gui label font
        orangegui.widgetLabel = cls.widgetLabel

    @classmethod
    def lineEdit(cls, widget, master, value, label=None, labelWidth=None,
             orientation='horizontal', box=None, callback=None,
             valueType=str, validator=None, controlWidth=None,
             callbackOnType=False, focusInCallback=None, **misc):

        ledit = orangegui.lineEdit(widget=widget,
                                    master=master,
                                    value=value,
                                    label=label,
                                    labelWidth=labelWidth,
                                    orientation=orientation,
                                    box=box,
                                    callback=callback,
                                    valueType=valueType,
                                    validator=validator,
                                    controlWidth=controlWidth,
                                    callbackOnType=callbackOnType,
                                    focusInCallback=focusInCallback,
                                    **misc)

        if value:
            if (valueType != str):
                ledit.setAlignment(Qt.AlignRight)

        ledit.setStyleSheet("background-color: white;")

        return ledit

    @classmethod
    def widgetBox(cls, widget, box=None, orientation='vertical', margin=None, spacing=4, height=None, width=None, **misc):

        box = orangegui.widgetBox(widget, box, orientation, margin, spacing, **misc)
        box.layout().setAlignment(Qt.AlignTop)

        if not height is None:
            box.setFixedHeight(height)
        if not width is None:
            box.setFixedWidth(width)

        return box

    @classmethod
    def tabWidget(cls, widget, height=None, width=None):
        tabWidget = orangegui.tabWidget(widget)

        if not height is None:
            tabWidget.setFixedHeight(height)
        if not width is None:
            tabWidget.setFixedWidth(width)

        tabWidget.setStyleSheet('QTabBar::tab::selected {background-color: #a6a6a6;}')

        return tabWidget

    @classmethod
    def createTabPage(cls, tabWidget, name, widgetToAdd=None, canScroll=False, height=None, width=None, isImage=False):

        tab = orangegui.createTabPage(tabWidget, name, widgetToAdd, canScroll)
        tab.layout().setAlignment(Qt.AlignTop)

        if not height is None:
            tab.setFixedHeight(height)
        if not width is None:
            tab.setFixedWidth(width)

        if isImage: tab.setStyleSheet("background-color: #FFFFFF;")

        return tab

    @classmethod
    def selectFileFromDialog(cls, widget, previous_file_path="", message="Select File", start_directory=".", file_extension_filter="*.*"):
        file_path = QFileDialog.getOpenFileName(widget, message, start_directory, file_extension_filter)[0]

        if not file_path is None and not file_path.strip() == "":
            return file_path
        else:
            return previous_file_path

    @classmethod
    def textArea(cls, height=None, width=None, readOnly=True):
        area = QTextEdit()
        area.setReadOnly(readOnly)
        area.setStyleSheet("background-color: white; font-family: Courier, monospace;")

        if not height is None: area.setFixedHeight(height)
        if not width is None: area.setFixedWidth(width)

        return area

    @classmethod
    def clearLayout(cls, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

# ------------------------------------
# UTILITY CLASS
# ------------------------------------

class ShowTextDialog(QDialog):

    def __init__(self, title, text, width=650, height=400, parent=None):
        QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        text_edit = QTextEdit("", self)
        text_edit.append(text)
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("background-color: white; font-family: Courier, monospace;")

        text_area = QScrollArea(self)
        text_area.setWidget(text_edit)
        text_area.setWidgetResizable(True)
        text_area.setFixedHeight(height)
        text_area.setFixedWidth(width)

        bbox = QDialogButtonBox(QDialogButtonBox.Ok)

        bbox.accepted.connect(self.accept)
        layout.addWidget(text_area)
        layout.addWidget(bbox)

    @classmethod
    def show_text(cls, title, text, width=650, height=400, parent=None):
        dialog = ShowTextDialog(title, text, width, height, parent)
        dialog.show()


class ConfirmTextDialog(QDialog):

    def __init__(self, title, text, text_before="", text_after="", width=650, height=400, parent=None):
        QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)

        label_before = QLabel()
        label_before.setText(text_before)
        layout.addWidget(label_before)

        text_edit = QTextEdit("", self)
        text_edit.append(text)
        text_edit.setReadOnly(True)

        text_area = QScrollArea(self)
        text_area.setWidget(text_edit)
        text_area.setWidgetResizable(True)
        text_area.setFixedHeight(height)
        text_area.setFixedWidth(width)

        layout.addWidget(text_area)

        label_after = QLabel()
        label_after.setText(text_after)
        layout.addWidget(label_after)

        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        layout.addWidget(bbox)

    @classmethod
    def confirm_text(cls, title, text, text_before="", text_after="", width=650, height=400, parent=None):
        return ConfirmTextDialog(title, text, text_before, text_after, width, height, parent).exec_() == QDialog.Accepted

class ConfirmDialog(QMessageBox):
    def __init__(self, parent, message, title):
        super(ConfirmDialog, self).__init__(parent)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.setIcon(QMessageBox.Question)
        self.setText(message)
        self.setWindowTitle(title)

    @classmethod
    def confirmed(cls, parent=None, message="Confirm Action?", title="Confirm Action"):
        return ConfirmDialog(parent, message, title).exec_() == QMessageBox.Ok

class OptionDialog(QMessageBox):

    selection = 0

    def __init__(self, parent, message, title, options, default):
        super(OptionDialog, self).__init__()
        self.setParent(parent)

        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.setIcon(QMessageBox.Question)
        self.setText(message)
        self.setWindowTitle(title)

        self.selection = default

        box = QWidget()
        box.setLayout(QGridLayout())
        box.setFixedHeight(40)

        box_combo = QWidget()
        combo = QComboBox(box_combo)
        combo.setEditable(False)
        combo.box = box_combo
        for item in options:
            combo.addItem(str(item))
        combo.setCurrentIndex(default)
        combo.currentIndexChanged.connect(self.set_selection)

        box.layout().addWidget(QLabel("Select Option"), 0, 0, 1, 1)
        box.layout().addWidget(box_combo, 0, 1, 1, 1)

        self.layout().addWidget(box, 1, 1, 1, 2)

    def set_selection(self, index):
        self.selection = index

    @classmethod
    def get_option(cls, parent=None, message="Select Option", title="Select Option", option=["No", "Yes"], default=0):
        dlg = OptionDialog(parent, message, title, option, default)
        if dlg.exec_() == QMessageBox.Ok:
            return dlg.selection
        else:
            return None

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from orangewidget.gui import notify_changed, CONTROLLED_ATTRIBUTES, ControlledAttributesDict

class InnerBox(QWidget):

    def __init__(self):
        super().__init__()

        setattr(self, CONTROLLED_ATTRIBUTES, ControlledAttributesDict(self))

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        notify_changed(self, key, value)

#######################################################################
#######################################################################
#######################################################################
# FIXING BUG ON MATPLOTLIB 2.0.0
#######################################################################
#######################################################################
#######################################################################

from silx.gui.plot.backends.BackendMatplotlib import BackendMatplotlibQt
from silx.gui.plot.PlotWindow import PlotWindow

class XRDAnalyzerBackendMatplotlibQt(BackendMatplotlibQt):

    def __init__(self, plot, parent=None):
        super().__init__(plot, parent)

    def _onMouseMove(self, event):
        try:
            super(XRDAnalyzerBackendMatplotlibQt, self)._onMouseMove(event)
        except ValueError as exception:
            if "Data has no positive values, and therefore can not be log-scaled" in str(exception):
                pass
            else:
                raise exception


def create_plot_window(parent=None, backend=None,
                       resetzoom=True, autoScale=True, logScale=True, grid=True,
                       curveStyle=True, colormap=True,
                       aspectRatio=True, yInverted=True,
                       copy=True, save=True, print_=True,
                       control=False, position=False,
                       roi=True, mask=True, fit=False):
    if backend is None:
        backend = XRDAnalyzerBackendMatplotlibQt

    return PlotWindow(parent=parent, backend=backend,
                      resetzoom=resetzoom, autoScale=autoScale, logScale=logScale, grid=grid,
                      curveStyle=curveStyle, colormap=colormap,
                      aspectRatio=aspectRatio, yInverted=yInverted,
                      copy=copy, save=save, print_=print_,
                      control=control, position=position,
                      roi=roi, mask=mask, fit=fit)
