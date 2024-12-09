"""
SVG export test
"""
from __future__ import division, print_function, absolute_import
from .pyqtgraph_vini import *
import tempfile
import os


app = mkQApp()


def test_plotscene():
    tempfilename = tempfile.NamedTemporaryFile(suffix='.svg').name
    print("using %s as a temporary file" % tempfilename)
    setConfigOption('foreground', (0,0,0))
    w = GraphicsWindow()
    w.show()        
    p1 = w.addPlot()
    p2 = w.addPlot()
    p1.plot([1,3,2,3,1,6,9,8,4,2,3,5,3], pen={'color':'k'})
    p1.setXRange(0,5)
    p2.plot([1,5,2,3,4,6,1,2,4,2,3,5,3], pen={'color':'k', 'cosmetic':False, 'width': 0.3})
    app.processEvents()
    app.processEvents()
    
    ex = exporters.SVGExporter(w.scene())
    ex.export(fileName=tempfilename)
    # clean up after the test is done
    os.unlink(tempfilename)

def test_simple():
    tempfilename = tempfile.NamedTemporaryFile(suffix='.svg').name
    print("using %s as a temporary file" % tempfilename)
    scene = QtWidgets.QGraphicsScene()

    grp2 = ItemGroup()
    scene.addItem(grp2)
    grp2.scale(100,100)

    rect3 = QtGui.QGraphicsRectItem(0,0,2,2)
    rect3.setPen(mkPen(width=1, cosmetic=False))
    grp2.addItem(rect3)

    ex = exporters.SVGExporter(scene)
    ex.export(fileName=tempfilename)
    os.unlink(tempfilename)
