import math
import numpy as np
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseButton
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.offsetbox import DraggableAnnotation
from matplotlib.text import Annotation
from scipy.signal import find_peaks

from app.model.measurement import Measurement
from app.model.measurements_table import MeasurementsTable


class AnnotationsFactory:
    PEAK_THRESHOLD = 5
    PRECISION_TO_PRINT = 2
    Y_OFFSET = 20
    X_OFFSET = 7
    NEXT_ANNOTATION_OFFSET = 50

    class MeasurementsProperties:
        def __init__(self, line: Line2D, annotation: Annotation = None, pinnedAnnotations=None, ):
            if pinnedAnnotations is None:
                pinnedAnnotations = []
            self.annotation: Annotation = annotation
            self.pinnedAnnotations: list[Annotation] = pinnedAnnotations
            self.line: Line2D = line
            self.peaksXCoordinates = None
            self.findPeaks()

        def findPeaks(self):
            x, y = self.line.get_data()
            minY = min(y)
            peaks, _ = find_peaks(y)
            series = np.array(y)
            peakX = []
            for peak in peaks:
                if series[peak] > minY * AnnotationsFactory.PEAK_THRESHOLD:
                    peakX.append(x[peak])
            self.peaksXCoordinates = peakX

    def __init__(self, ax: Axes, measurementsTable: MeasurementsTable):
        self.measurementsTable = measurementsTable
        self.ax = ax
        self.fig: Figure = ax.get_figure()
        self.annotationXOffset = -20
        self.measurementsProperties: dict[Measurement, AnnotationsFactory.MeasurementsProperties] = {}
        self.draggableAnnotation = None
        self.onlyPeaks = False
        self.wasPressedWithNoMotion = False
        self.dragging = False
        self.measurementsTable.dataChanged.connect(self.updateSelectedLinesAnnotationsCoordinates)

    def addNewLine(self, measurement: Measurement, line: Line2D):
        annotation = self.createAnnotationForLine(line, self.annotationXOffset)
        self.measurementsProperties[measurement] = AnnotationsFactory.MeasurementsProperties(line, annotation, [])

    def removeMeasurement(self, measurement: Measurement):
        measurementProperties = self.measurementsProperties[measurement]
        for pinnedAnnotation in measurementProperties.pinnedAnnotations:
            pinnedAnnotation.remove()
        measurementProperties.annotation.remove()
        del self.measurementsProperties[measurement]

    def updateSelectedLinesAnnotationsCoordinates(self, _):
        selectedMeasurements = self.measurementsTable.getSelectedMeasurements()
        if len(selectedMeasurements) == 0:
            return
        someAnnotation = self.measurementsProperties[selectedMeasurements[0]].annotation
        scale = self.ax.get_xscale()
        if scale == 'log':
            position = math.log((someAnnotation.xy[0] / self.ax.get_xlim()[0]),
                                (self.ax.get_xlim()[1] / self.ax.get_xlim()[0]))
        else:
            position = (someAnnotation.xy[0] - self.ax.get_xlim()[0]) / \
                       (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
        offset = -position * AnnotationsFactory.NEXT_ANNOTATION_OFFSET * len(selectedMeasurements)
        offset += AnnotationsFactory.X_OFFSET
        for (measurement, measurementProperties) in self.measurementsProperties.items():
            annotation = measurementProperties.annotation
            if measurement in selectedMeasurements:
                annotation.set_visible(True)
                annotation.xyann = (offset, AnnotationsFactory.Y_OFFSET)
                offset += AnnotationsFactory.NEXT_ANNOTATION_OFFSET
            else:
                annotation.set_visible(False)

    def createAnnotationForLine(self, line, xtext) -> Annotation:
        newAnnotation: Annotation = self.ax.annotate('', xy=(0, 0), xytext=(xtext, AnnotationsFactory.Y_OFFSET),
                                                     textcoords='offset points', bbox=dict(boxstyle='round', fc='w'),
                                                     arrowprops=dict(arrowstyle='-', color='#444444'))
        newAnnotation.get_bbox_patch().set_color(line.get_color())
        newAnnotation.get_bbox_patch().set_alpha(0.4)
        return newAnnotation

    def hideAnnotations(self):
        for annotation in [mp.annotation for mp in self.measurementsProperties.values()]:
            annotation.set_visible(False)
        self.drawAllArtistsExceptAxes()

    def drawAllArtistsExceptAxes(self):
        self.ax.draw_artist(self.ax.patch)
        for line in [mp.line for mp in self.measurementsProperties.values()]:
            self.ax.draw_artist(line)
        for mp in self.measurementsProperties.values():
            for annotation in mp.pinnedAnnotations:
                self.ax.draw_artist(annotation)
            self.ax.draw_artist(mp.annotation)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def changeMeasurementAnnotationsColor(self, measurement):
        mp = self.measurementsProperties[measurement]
        for pinnedAnnotation in mp.pinnedAnnotations:
            pinnedAnnotation.get_bbox_patch().set_color(mp.line.get_color())
            pinnedAnnotation.get_bbox_patch().set_alpha(0.4)
        mp.annotation.get_bbox_patch().set_color(mp.line.get_color())
        mp.annotation.get_bbox_patch().set_alpha(0.4)

    def setup(self):

        def update_annot(annotation, x_cord, y_cord):
            annotation.xy = (x_cord, y_cord)
            text = f'x: {x_cord:.0f}\ny: {y_cord:.{self.PRECISION_TO_PRINT}f}'
            annotation.set_text(text)

        def hover(event):
            self.wasPressedWithNoMotion = False
            if event.inaxes == self.ax and not self.dragging:
                selectedMeasurements = self.measurementsTable.getSelectedMeasurements()
                scale = self.ax.get_xscale()
                if scale == 'log':
                    position = math.log((event.xdata / self.ax.get_xlim()[0]),
                                        (self.ax.get_xlim()[1] / self.ax.get_xlim()[0]))
                else:
                    position = (event.xdata - self.ax.get_xlim()[0]) / \
                               (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])
                offset = -position * AnnotationsFactory.NEXT_ANNOTATION_OFFSET * len(selectedMeasurements)
                offset += AnnotationsFactory.X_OFFSET
                for (measurement, measurementProperties) in self.measurementsProperties.items():
                    if measurement not in selectedMeasurements:
                        continue
                    annotation = measurementProperties.annotation
                    x, y = measurementProperties.line.get_data()
                    eventX = event.xdata
                    if self.onlyPeaks:
                        xArray = np.asarray(measurementProperties.peaksXCoordinates)
                    else:
                        xArray = np.asarray(x)
                    ind = (np.abs(xArray - eventX)).argmin()
                    x_cord = xArray[ind]
                    y_ind = list(x).index(x_cord)
                    y_cord = y[y_ind]
                    update_annot(annotation, x_cord, y_cord)
                    if annotation.xy not in [annotation_.xy for annotation_ in measurementProperties.pinnedAnnotations]:
                        annotation.set_visible(True)
                        annotation.xyann = (offset, 20)
                    else:
                        annotation.set_visible(False)
                    offset += AnnotationsFactory.NEXT_ANNOTATION_OFFSET
                self.drawAllArtistsExceptAxes()
            else:
                self.hideAnnotations()

        def onPress(event):
            self.wasPressedWithNoMotion = True
            if event.inaxes != self.ax:
                return
            self.draggableAnnotation = None
            if event.button == MouseButton.LEFT:
                for measurementProperties in self.measurementsProperties.values():
                    for annotation in measurementProperties.pinnedAnnotations:
                        if annotation.contains(event)[0]:
                            self.draggableAnnotation = annotation
                            self.hideAnnotations()
                            self.dragging = True
                            return

        def onRelease(event):
            """On release, we pin or close annotation"""
            if event.button == MouseButton.RIGHT:
                closePinnedAnnotation(event)
            elif event.button == MouseButton.LEFT and self.wasPressedWithNoMotion:
                for measurementProperties in self.measurementsProperties.values():
                    pinAnnotation(measurementProperties)
            self.draggableAnnotation = None
            self.dragging = False
            return

        def closePinnedAnnotation(event):
            for measurementProperties in self.measurementsProperties.values():
                removedAnnotations = []
                for annotation in measurementProperties.pinnedAnnotations:
                    if annotation.contains(event)[0]:
                        measurementProperties.pinnedAnnotations.remove(annotation)
                        annotation.set_visible(False)
                        self.drawAllArtistsExceptAxes()
                        annotation.remove()
                        removedAnnotations.append(annotation)
                        return
                for removedAnnotation in removedAnnotations:
                    measurementProperties.pinnedAnnotations.remove(removedAnnotation)

        def pinAnnotation(measurementProperties):
            annotationToPin = measurementProperties.annotation
            if annotationToPin.xy not in [annotation_.xy for annotation_ in measurementProperties.pinnedAnnotations]:
                annotationToPin.draggable()
                measurementProperties.pinnedAnnotations.append(annotationToPin)
                newAnnotation = self.createAnnotationForLine(measurementProperties.line, annotationToPin.xyann[0])
                newAnnotation.set_visible(False)
                measurementProperties.annotation = newAnnotation

        self.fig.canvas.mpl_connect('motion_notify_event', hover)
        self.fig.canvas.mpl_connect('button_press_event', onPress)
        self.fig.canvas.mpl_connect('button_release_event', onRelease)


def myOnPick(self, evt):
    """Pick annotations only on left mouse click"""
    if evt.mouseevent.button == MouseButton.LEFT:
        super(DraggableAnnotation, self).on_pick(evt)


DraggableAnnotation.on_pick = myOnPick
