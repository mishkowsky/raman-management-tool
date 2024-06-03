import sys
import matplotlib
import numpy as np
from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QCheckBox
from loguru import logger
from matplotlib._afm import _to_int
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DraggableAnnotation
from matplotlib.text import Annotation
from scipy.signal import find_peaks

from app.model.measurement import Measurement
from app.model.measurements_table import MeasurementsTable
from app.view.modules.styles import MATPLOT_WIDGET_STYLESHEET
from app.view.widgets.matplot.annotations_factory import AnnotationsFactory
from app.view.widgets.matplot.pan_factory import PanFactory
from app.view.widgets.matplot.zoom_factory import ZoomFactory

matplotlib.use('Qt5Agg')


class CustomToolbar(NavigationToolbar):

    def __init__(self, canvas_, parent_):

        requiredTools = ['Brush', 'Delete', 'Customize', 'Home', 'Back', 'Forward', 'Pan', 'Zoom']

        index = self.toolitems.index(('Save', 'Save the figure', 'filesave', 'save_figure'))
        self.toolitems.insert(index, ('Brush', 'Choose color for selected lines', 'brush', 'brush_lines'))
        self.toolitems.insert(index, ('Resize', 'Resize vertical axes', 'resize', 'resize_y_axes'))
        self.toolitems.append(('Delete', 'Remove selected lines from plot', 'delete', 'remove_lines'))
        self.toolitems.remove((None, None, None, None))  # remove empty separators
        self.toolitems.remove((None, None, None, None))  # remove empty separators

        toolsToRemove = []
        for text, tooltip_text, image_file, callback in self.toolitems:
            if text is not None and text not in requiredTools:
                toolsToRemove.append((text, tooltip_text, image_file, callback))
        for tool in toolsToRemove:
            self.toolitems.remove(tool)

        NavigationToolbar.__init__(self, canvas_, parent_, False)
        icons_buttons = {
            'Home': QtGui.QIcon(':/icons/images/icons/cil-home.png'),
            'Back': QtGui.QIcon(":/icons/images/icons/cil-action-undo.png"),
            'Forward': QtGui.QIcon(':/icons/images/icons/cil-action-redo.png'),
            'Pan': QtGui.QIcon(':/icons/images/icons/cil-move.png'),
            'Zoom': QtGui.QIcon(':/icons/images/icons/cil-magnifying-glass.png'),
            'Subplots': QtGui.QIcon(':/icons/images/icons/cil-equalizer.png'),
            'Customize': QtGui.QIcon(':/icons/images/icons/cil-chart-line-no-arrow.png'),
            'Save': QtGui.QIcon(':/icons/images/icons/cil-save.png'),
            'Delete': QtGui.QIcon(':/icons/images/icons/cil-x.png'),
            'Brush': QtGui.QIcon(':/icons/images/icons/cil-paint-bucket.png'),
            'Resize': QtGui.QIcon(':/icons/images/icons/cil-vertical-resize.png')
        }

        for action in self.actions():
            if action.text() in icons_buttons:
                action.setIcon(icons_buttons.get(action.text(), QtGui.QIcon()))

        self.checkboxTightLayout = QCheckBox('Tight layout')
        self.checkboxPeaks = QCheckBox('Only peaks')
        self.checkboxPeaks.stateChanged.connect(canvas_.setOnlyPeaks)
        self.checkboxTightLayout.setChecked(canvas_.tightLayout)
        self.checkboxTightLayout.stateChanged.connect(canvas_.setTightLayout)
        self.addSeparator()
        self.addWidget(self.checkboxPeaks)

        self.locLabel = QtWidgets.QLabel("", self)
        self.locLabel.setAlignment(QtCore.Qt.AlignmentFlag(
            _to_int(QtCore.Qt.AlignmentFlag.AlignRight) |
            _to_int(QtCore.Qt.AlignmentFlag.AlignVCenter)))

        self.locLabel.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Ignored,
        ))
        labelAction = self.addWidget(self.locLabel)
        labelAction.setVisible(True)
        self.coordinates = True

    @staticmethod
    def _mouse_event_to_message(event):
        if event.inaxes and event.inaxes.get_navigate():
            return f'x={event.xdata:.0f} y={event.ydata:.{AnnotationsFactory.PRECISION_TO_PRINT}f}'
        else:
            return ''

    def remove_lines(self):
        pass

    def brush_lines(self):
        pass

    def resize_y_axes(self):
        pass


class MatplotCanvas(FigureCanvasQTAgg):
    tightLayout = True
    onlyPeaks = False

    def __init__(self, parent=None, width=5, height=4, dpi=100, measurementsTableModel: MeasurementsTable = None):
        import app.view.widgets.matplot.figure_options
        self.measurementsTable = measurementsTableModel
        self.addedLines: dict[Measurement, Line2D] = {}

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor('none')
        self.fig.set_edgecolor('none')

        self.axes: Axes = self.fig.add_subplot(111)
        self.axes.set_xscale('log')
        minX = min(Measurement.SPECTRUM_FREQUENCIES)
        maxX = max(Measurement.SPECTRUM_FREQUENCIES)
        self.axes.set_xlim(left=minX, right=maxX)
        self.axes.set_facecolor('white')
        self.axes.spines['bottom'].set_color('#DDDDDD')
        self.axes.spines['top'].set_color('#DDDDDD')
        self.axes.spines['right'].set_color('#DDDDDD')
        self.axes.spines['left'].set_color('#DDDDDD')
        self.axes.tick_params(axis='x', colors='#DDDDDD', which='both')
        self.axes.tick_params(axis='y', colors='#DDDDDD')
        self.axes.xaxis.label.set_color('#DDDDDD')
        self.axes.yaxis.label.set_color('#DDDDDD')

        self.annotationsFactory = AnnotationsFactory(self.axes, measurementsTableModel)
        self.annotationsFactory.setup()
        ZoomFactory(minX, maxX).zoom_factory(self.axes, self.annotationsFactory)
        PanFactory(minX, maxX, annotationFactory=self.annotationsFactory).pan_factory(self.axes)

        super(MatplotCanvas, self).__init__(self.fig)
        self.setStyleSheet('none')
        self.fig.tight_layout()
        self.fig.canvas.draw()

    def leaveEvent(self, event):
        self.annotationsFactory.hideAnnotations()
        return super(MatplotCanvas, self).leaveEvent(event)

    def resizeEvent(self, event):
        if self.tightLayout:
            self.fig.tight_layout()
            self.fig.canvas.draw()
        super().resizeEvent(event)

    def setTightLayout(self):
        newTightLayout = not self.tightLayout
        if newTightLayout and not self.tightLayout:
            self.fig.tight_layout()
            self.fig.canvas.draw()
        self.tightLayout = newTightLayout

    def setOnlyPeaks(self):
        newOnlyPeaks = not self.onlyPeaks
        self.annotationsFactory.onlyPeaks = newOnlyPeaks
        self.onlyPeaks = newOnlyPeaks

    def addMeasurementGraphic(self, measurement: Measurement) -> Line2D:
        y = measurement.spectrumList
        x = Measurement.SPECTRUM_FREQUENCIES[0:len(y)]
        line, = self.axes.plot(x, y)
        self.addedLines[measurement] = line
        self.fig.canvas.draw()
        self.annotationsFactory.addNewLine(measurement, line)
        self.resizeVerticalAxes()
        return line

    def removeMeasurementLines(self, measurements: list[Measurement]):
        for measurement in measurements:
            logger.debug(f'REMOVING LINE WITH NAME {measurement.name}')
            line = self.addedLines[measurement]
            line.remove()
            self.annotationsFactory.removeMeasurement(measurement)  # removeLine(line)
            del self.addedLines[measurement]
        self.fig.canvas.draw()
        if not self.axes.lines or len(self.axes.lines) == 0:
            self.annotationsFactory.hideAnnotations()
        self.resizeVerticalAxes()

    def changeSelectedLinesColor(self, color):
        selectedMeasurements = self.measurementsTable.getSelectedMeasurements()
        for selectedMeasurement in selectedMeasurements:
            line = self.addedLines[selectedMeasurement]
            line.set_color(color)
            self.annotationsFactory.changeMeasurementAnnotationsColor(selectedMeasurement)
        self.fig.canvas.draw()

    def resizeVerticalAxes(self):
        maxY = -1
        for line in self.addedLines.values():
            yData = line.get_ydata()
            maximum = yData.max()
            if maximum > maxY:
                maxY = maximum
        if maxY == -1:
            maxY = 1
        logger.debug(f'SETTING BOUNDS TO [{0 - 0.05 * maxY}; {maxY}]')
        self.axes.set_ybound(lower=0 - 0.05 * maxY, upper=maxY * 1.25)
        self.fig.canvas.draw()


class MatplotLayout:

    def __init__(self, parentWidget, measurementsTableModel: MeasurementsTable):
        self.canvas: MatplotCanvas = MatplotCanvas(self, width=5, height=4, dpi=100,
                                                   measurementsTableModel=measurementsTableModel)
        self.toolbar = CustomToolbar(self.canvas, parentWidget)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

    def getLayout(self):
        return self.layout
