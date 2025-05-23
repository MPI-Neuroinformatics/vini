"""
This module exists to smooth out some of the differences between PySide and PyQt4:

* Automatically import either PyQt4 or PySide depending on availability
* Allow to import QtCore/QtGui pyqtgraph_vini.Qt without specifying which Qt wrapper
  you want to use.
* Declare QtCore.Signal, .Slot in PyQt4
* Declare loadUiType function for Pyside

"""

import os, sys, re, time

from .python2_3 import asUnicode

PYSIDE = 'PySide'
PYQT4 = 'PyQt4'
PYQT5 = 'PyQt5'
PYQT6 = 'PyQt6'


QT_LIB = os.getenv('PYQTGRAPH_QT_LIB')

## Automatically determine whether to use PyQt or PySide (unless specified by
## environment variable).
## This is done by first checking to see whether one of the libraries
## is already imported. If not, then attempt to import PyQt4, then PySide.
if QT_LIB is None:
    libOrder = [PYQT6, PYSIDE, PYQT5]

    for lib in libOrder:
        if lib in sys.modules:
            QT_LIB = lib
            break

if QT_LIB is None:
    for lib in libOrder:
        try:
            __import__(lib)
            QT_LIB = lib
            break
        except ImportError:
            pass

# print("QT_LIB {}".format(QT_LIB))


if QT_LIB is None:
    raise Exception("PyQtGraph requires one of PyQt5, PyQt6 or PySide; none of these packages could be imported.")


class FailedImport(object):
    """Used to defer ImportErrors until we are sure the module is needed.
    """
    def __init__(self, err):
        self.err = err
        
    def __getattr__(self, attr):
        raise self.err


if QT_LIB == PYSIDE:
    from PySide import QtGui, QtCore, QtOpenGL, QtSvg
    try:
        from PySide import QtTest
        if not hasattr(QtTest.QTest, 'qWait'):
            @staticmethod
            def qWait(msec):
                start = time.time()
                QtGui.QApplication.processEvents()
                while time.time() < start + msec * 0.001:
                    QtGui.QApplication.processEvents()
            QtTest.QTest.qWait = qWait
                
    except ImportError:
        pass
    import PySide
    try:
        from PySide import shiboken
        isQObjectAlive = shiboken.isValid
    except ImportError:
        def isQObjectAlive(obj):
            try:
                if hasattr(obj, 'parent'):
                    obj.parent()
                elif hasattr(obj, 'parentItem'):
                    obj.parentItem()
                else:
                    raise Exception("Cannot determine whether Qt object %s is still alive." % obj)
            except RuntimeError:
                return False
            else:
                return True
    
    VERSION_INFO = 'PySide ' + PySide.__version__
    
    # Make a loadUiType function like PyQt has
    
    # Credit:
    # http://stackoverflow.com/questions/4442286/python-code-genration-with-pyside-uic/14195313#14195313

    class StringIO(object):
        """Alternative to built-in StringIO needed to circumvent unicode/ascii issues"""
        def __init__(self):
            self.data = []
        
        def write(self, data):
            self.data.append(data)
            
        def getvalue(self):
            return ''.join(map(asUnicode, self.data)).encode('utf8')
        
    def loadUiType(uiFile):
        """
        Pyside "loadUiType" command like PyQt4 has one, so we have to convert
        the ui file to py code in-memory first and then execute it in a
        special frame to retrieve the form_class.

        from stackoverflow: http://stackoverflow.com/a/14195313/3781327

        seems like this might also be a legitimate solution, but I'm not sure
        how to make PyQt4 and pyside look the same...
            http://stackoverflow.com/a/8717832
        """
        import pysideuic
        import xml.etree.ElementTree as xml
        #from io import StringIO
        
        parsed = xml.parse(uiFile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text
        
        with open(uiFile, 'r') as f:
            o = StringIO()
            frame = {}

            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec(pyc, frame)

            #Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('QtGui.%s'%widget_class)

        return form_class, base_class



elif QT_LIB == PYQT5:
    
    # We're using PyQt5 which has a different structure so we're going to use a shim to
    # recreate the Qt4 structure for Qt5
    from PyQt5 import QtGui, QtCore, QtWidgets, uic
    try:
        from PyQt5 import QtSvg
    except ImportError:
        pass
    try:
        from PyQt5 import QtOpenGL
    except ImportError:
        pass
    try:
        from PyQt5 import QtTest
        QtTest.QTest.qWaitForWindowShown = QtTest.QTest.qWaitForWindowExposed
    except ImportError:
        pass

    # Re-implement deprecated APIs

    __QGraphicsItem_scale = QtWidgets.QGraphicsItem.scale

    def scale(self, *args):
        if args:
            sx, sy = args
            tr = self.transform()
            tr.scale(sx, sy)
            self.setTransform(tr)
        else:
            return __QGraphicsItem_scale(self)

    QtWidgets.QGraphicsItem.scale = scale

    def rotate(self, angle):
        tr = self.transform()
        tr.rotate(angle)
        self.setTransform(tr)
    QtWidgets.QGraphicsItem.rotate = rotate

    def translate(self, dx, dy):
        tr = self.transform()
        tr.translate(dx, dy)
        self.setTransform(tr)
    QtWidgets.QGraphicsItem.translate = translate

    def setMargin(self, i):
        self.setContentsMargins(i, i, i, i)
    QtWidgets.QGridLayout.setMargin = setMargin

    def setResizeMode(self, *args):
        self.setSectionResizeMode(*args)
    QtWidgets.QHeaderView.setResizeMode = setResizeMode

    
    '''QtGui.QApplication = QtWidgets.QApplication
    QtGui.QGraphicsScene = QtWidgets.QGraphicsScene
    QtGui.QGraphicsObject = QtWidgets.QGraphicsObject
    QtGui.QGraphicsWidget = QtWidgets.QGraphicsWidget'''

    QtWidgets.QApplication.setGraphicsSystem = None
    
    # Import all QtWidgets objects into QtGui
    for o in dir(QtWidgets):
        if o.startswith('Q'):
            setattr(QtGui, o, getattr(QtWidgets,o) )

    module_whitelist = [
        "QAction",
        "QActionGroup",
        "QFileSystemModel",
        "QShortcut",
        "QUndoCommand",
        "QUndoGroup",
        "QUndoStack",
    ]
    for module in module_whitelist:
        attr = getattr(QtWidgets, module)
        setattr(QtGui, module, attr)
    
    VERSION_INFO = 'PyQt5 ' + QtCore.PYQT_VERSION_STR + ' Qt ' + QtCore.QT_VERSION_STR





elif QT_LIB == PYQT6:
    
    ''' # We're using PyQt6 which has a different structure so we're going to use a shim to
    # recreate the Qt4 structure for Qt5
    from PyQt6 import QtGui, QtCore, QtWidgets, uic
    try:
        from PyQt6 import QtSvg
    except ImportError:
        pass
    try:
        from PyQt6 import QtOpenGL
    except ImportError:
        pass
    try:
        from PyQt6 import QtTest
        QtTest.QTest.qWaitForWindowShown = QtTest.QTest.qWaitForWindowExposed
    except ImportError:
        pass'''

    from PyQt6 import QtGui, QtCore, QtWidgets, uic, sip

    try:
        from PyQt6 import QtSvg
    except ImportError as err:
        QtSvg = FailedImport(err)
    try:
        from PyQt6 import QtOpenGLWidgets
    except ImportError as err:
        QtOpenGLWidgets = FailedImport(err)
    try:
        from PyQt6 import QtTest
    except ImportError as err:
        QtTest = FailedImport(err)

    # Re-implement deprecated APIs

    __QGraphicsItem_scale = QtWidgets.QGraphicsItem.scale

    def scale(self, *args):
        if args:
            sx, sy = args
            tr = self.transform()
            tr.scale(sx, sy)
            self.setTransform(tr)
        else:
            return __QGraphicsItem_scale(self)

    QtWidgets.QGraphicsItem.scale = scale

    def rotate(self, angle):
        tr = self.transform()
        tr.rotate(angle)
        self.setTransform(tr)
    QtWidgets.QGraphicsItem.rotate = rotate

    def translate(self, dx, dy):
        tr = self.transform()
        tr.translate(dx, dy)
        self.setTransform(tr)
    QtWidgets.QGraphicsItem.translate = translate

    def setMargin(self, i):
        self.setContentsMargins(i, i, i, i)
    QtWidgets.QGridLayout.setMargin = setMargin

    def setResizeMode(self, *args):
        self.setSectionResizeMode(*args)
    QtWidgets.QHeaderView.setResizeMode = setResizeMode

    QtWidgets.QApplication.setGraphicsSystem = None
    
    # Import all QtWidgets objects into QtGui
    for o in dir(QtWidgets):
        if o.startswith('Q'):
            setattr(QtGui, o, getattr(QtWidgets,o) )
    
    if not isinstance(QtOpenGLWidgets, FailedImport):
        QtWidgets.QOpenGLWidget = QtOpenGLWidgets.QOpenGLWidget
    
    VERSION_INFO = 'PyQt6 ' + QtCore.PYQT_VERSION_STR + ' Qt ' + QtCore.QT_VERSION_STR


else:
    raise ValueError("Invalid Qt lib '%s'" % QT_LIB)

# Common to PyQt4 and 6
if QT_LIB.startswith('PyQt'):
    if QT_LIB != PYQT6:
        import sip
        def isQObjectAlive(obj):
            return not sip.isdeleted(obj)
    else:
        from PyQt6 import sip
        def isQObjectAlive(obj):
            return not sip.isdeleted(obj)
    
    loadUiType = uic.loadUiType

    QtCore.Signal = QtCore.pyqtSignal
    
if QT_LIB in [PYQT5, PYQT6]:
    QtVersion = QtCore.QT_VERSION_STR

    # PyQt, starting in v5.5, calls qAbort when an exception is raised inside
    # a slot. To maintain backward compatibility (and sanity for interactive
    # users), we install a global exception hook to override this behavior.
    if sys.excepthook == sys.__excepthook__:
        sys_excepthook = sys.excepthook
        def pyqt_qabort_override(*args, **kwds):
            return sys_excepthook(*args, **kwds)
        sys.excepthook = pyqt_qabort_override
    
    def isQObjectAlive(obj):
        return not sip.isdeleted(obj)
    
    loadUiType = uic.loadUiType

    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot

    
## Make sure we have Qt >= 4.7
versionReq = [4, 7]
USE_PYSIDE = QT_LIB == PYSIDE
USE_PYQT4 = QT_LIB == PYQT4
USE_PYQT5 = QT_LIB == PYQT5
USE_PYQT6 = QT_LIB == PYQT6
QtVersion = PySide.QtCore.__version__ if QT_LIB == PYSIDE else QtCore.QT_VERSION_STR
m = re.match(r'(\d+)\.(\d+).*', QtVersion)
if m is not None and list(map(int, m.groups())) < versionReq:
    print(list(map(int, m.groups())))
    raise Exception('pyqtgraph requires Qt version >= %d.%d  (your version is %s)' % (versionReq[0], versionReq[1], QtVersion))