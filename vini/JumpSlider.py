from .pyqtgraph_vini.Qt import QtCore, QtGui


class JumpSlider(QtGui.QSlider):
    """
    Jump slider for functional image frame selection.
    Allows to click to a desired position.
    """

    def mousePressEvent(self, ev):
        """ Jump to click position """
        if hasattr(ev, 'position'): 
            x_pos = round(ev.position().x())
        else:
            x_pos = ev.x()
        self.setValue(QtGui.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), x_pos-8, self.width()-16))
        self.sliderPressed.emit()

    def mouseReleaseEvent(self, ev):
        self.sliderReleased.emit()

    def mouseMoveEvent(self, ev):
        """ Jump to pointer position while moving """
        if hasattr(ev, 'position'): 
            x_pos = round(ev.position().x())
        else:
            x_pos = ev.x()
        self.setValue(QtGui.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), x_pos-8, self.width()-16))
