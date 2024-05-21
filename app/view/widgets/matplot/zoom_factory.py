
class ZoomFactory:
    def __init__(self, minX, maxX, minY=-1, maxY=float('inf')):
        self.maxX = maxX
        self.minX = minX
        self.maxY = maxY
        self.minY = minY

        self.cur_x_lim = None

    def zoom_factory(self, ax, base_scale=1.35):
        def zoom(event):
            cur_x_lim = ax.get_xlim()
            xdata = event.xdata
            if event.button == 'up':
                scale_factor = base_scale
            elif event.button == 'down':
                scale_factor = 1 / base_scale
            else:
                return
            scaling = ax.get_xscale()
            if scaling == 'linear':
                newRightX = xdata + (cur_x_lim[1] - xdata) / scale_factor
                newLeftX = xdata - (xdata - cur_x_lim[0]) / scale_factor
            elif scaling == 'log':
                newRightX = xdata * pow(cur_x_lim[1] / xdata, 1 / scale_factor)
                newLeftX = xdata / pow(xdata / cur_x_lim[0], 1 / scale_factor)
            else:
                return
            newRightX = min(self.maxX, newRightX)
            newLeftX = max(self.minX, newLeftX)
            ax.set_xlim([newLeftX, newRightX])
            ax.figure.canvas.draw()

        fig = ax.get_figure()  # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

