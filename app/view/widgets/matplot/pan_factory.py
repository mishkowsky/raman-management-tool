from matplotlib.backend_bases import MouseButton
from matplotlib.text import Annotation


class PanFactory:
    def __init__(self, minX, maxX, minY=-1, maxY=float('inf'), annotationFactory=None):
        self.maxX = maxX
        self.minX = minX
        self.maxY = maxY
        self.minY = minY
        self.press = False
        self.cur_x_lim = None
        self.cur_y_lim = None
        self.xPress = None
        self.yPress = None
        self.annotations = annotationFactory
        self.annotationToMove: Annotation | None = None

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax:
                return
            self.cur_x_lim = ax.get_xlim()
            self.press = True
            self.xPress, self.yPress = event.xdata, event.ydata

        def onRelease(_):
            self.press = False

        def onMotion(event):
            if not self.press or event.inaxes != ax or event.button != MouseButton.LEFT or self.annotations.dragging:
                return

            scaling = ax.get_xscale()
            if scaling == 'linear':
                dx = self.xPress - event.xdata
                self.new_x_lim = self.cur_x_lim + dx
                correction = 0
                if self.new_x_lim[0] < self.minX:
                    correction = self.minX - self.new_x_lim[0]
                if self.new_x_lim[1] > self.maxX:
                    correction = self.maxX - self.new_x_lim[1]
                self.cur_x_lim = (self.cur_x_lim[0] + dx + correction, self.cur_x_lim[1] + dx + correction)
            elif scaling == 'log':
                dx = self.xPress / event.xdata
                self.new_x_lim = (self.cur_x_lim[0] * dx, self.cur_x_lim[1] * dx)
                correction = 1
                if self.new_x_lim[0] < self.minX:
                    correction = self.minX / self.new_x_lim[0]
                if self.new_x_lim[1] > self.maxX:
                    correction = self.maxX / self.new_x_lim[1]
                self.cur_x_lim = (self.cur_x_lim[0] * dx * correction, self.cur_x_lim[1] * dx * correction)
            else:
                return

            # if self.annotations.dragging:
            #     pass
            # else:
            ax.set_xlim(self.cur_x_lim)
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        # return the function
        return onMotion
