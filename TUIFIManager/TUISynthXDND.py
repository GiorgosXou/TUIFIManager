"""
Part of TUItilities, TUI Synthetic/virtual XDND "protocol"
May god forgive me for what you are about to see...
"""

from pynput.mouse import Button, Controller, Listener
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QMimeData, QUrl, QObject, Signal
from PySide6 import QtCore
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDrag
from Xlib import display
from time import sleep
import threading
import sys
import copy
import re



class writerr(object):
    def write(self, data): # Ignore warning
        if not data == "sys:1: Warning: g_main_context_pop_thread_default: assertion 'stack != NULL' failed\n":
            print(data)

sys.stderr = writerr() # WARN: pyside\qt getting wild, cause cutie aint thread safe | VERY SuS thought

# os.environ['QT_LOGGING_RULES'] = 'qt.qpa.input*.debug=false; *.debug=false; qt.*.debug=false; driver.*.debug=false'
# os.environ["QT_LOGGING_RULES"] = '*.debug=false;qt.accessibility.cache.warning=false;qt.qpa.events.warning=false;qt.qpa.fonts.warning=false;qt.qpa.gl.warning=false;qt.qpa.input.devices.warning=false;qt.qpa.screen.warning=false;qt.qpa.xcb.warning=false;qt.text.font.db.warning=false;qt.xkb.compose.warning=false' # https://stackoverflow.com/questions/68809878/how-do-you-silence-console-messages-from-matplotlib-with-pyqt5-backend



class DropWindow(QMainWindow):
    def __init__(self, on_drop):
        super().__init__()
        self.setWindowFlag(Qt.X11BypassWindowManagerHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowOpacity(0) 
        self.setAcceptDrops(True)
        self.resize(9,9)
        self.perform_drop = on_drop
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # 128 is the alpha value for 50% opacity
        

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()


    def unescape(self, s):
        s = s.replace("&apos;", "'")
        s = s.replace("&quot;", '"')
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&amp;", "&") # this has to be last
        return s


    pattern = re.compile(r'src="([^"]+)"')
    __tmp_match = None
    def extract_src(self, html_string):
        match = self.pattern.search(html_string)
        if match:
            self.__tmp_match = self.unescape(match.group(1))
            return self.__tmp_match
        else:
            self.__tmp_match = None
            return None


    def dropEvent(self, event: QDropEvent): # https://stackoverflow.com/questions/74352310/how-to-get-an-image-that-dragged-and-dropped-from-the-browser-to-the-droparea-qm
        event.accept()
        f = event.mimeData()
        if f.html() and self.extract_src(f.html()): # and because it might be None
            if self.__tmp_match.startswith('http'):
                self.perform_drop(self.__tmp_match, 0)
            else:
                self.perform_drop(self.__tmp_match, 2)
        elif f.text():
            if not f.text().startswith("file://"):
                self.perform_drop(f.text(), 0)
            else:
                self.perform_drop(QUrl(f.text()).toLocalFile(), 1)
            # print("Dropped  URL: ", event.mimeData().text())
        else:
            # self.perform_drop(event.mimeData().urls(), 1)
            for url in event.mimeData().urls():
                self.perform_drop(url.toLocalFile(), 1)



d           = display.Display()
root        = d.screen().root
self_window = d.get_input_focus().focus # or parrent but if not parrent is root (because some windows managers such i3 use containers\windows)

listener = Listener()
listener.start()



class MyObject(QObject):
    my_signal = Signal(list) # Define a custom signal
    def __init__(self): super().__init__()
    def begin_virtial_drag(self, files): self.my_signal.emit(files) # Emit the signal with some data



def qtMessageHandler(type: QtCore.QtMsgType, context: QtCore.QMessageLogContext, msg: str):
    pass



class SyntheticXDND:

    def is_mouse_cursor_inside(self, geometry, x,y):
        return (x > geometry.x and x < geometry.x + geometry.width and y > geometry.y and y < geometry.y + geometry.height)

    def get_self_geometry(self):
        if self_window.query_tree().parent != root: # at least for i3 (because some windows managers such i3 use plus containers\windows)
             return self_window.query_tree().parent.get_geometry()
        else: # I tried to be inclusive, even thought I have no idea of how other window managers might handle this
             return self_window.get_geometry()


    files = None

    def dnd_slot(self, files): # I'm both proud and ashamed for this whole xdnd "code" lol
        mime_data = QMimeData()
        mime_data.setUrls(files) 
        drag = QDrag(self.w)
        drag.setMimeData(mime_data)
        drag.exec()


    def perform_virtual_file_drag(self, x,y):
        files = self.__on_drag() # just... don't... it works that way... cutie\qt has thread issues
        if not files:return
        self.obj.begin_virtial_drag(files)  # This will emit the signal with __on_drag selected files
        # sleep(.3) # ^^^ debatable... but what can i do? Also SuS...
        # move mouse slightly to wake up the event
        self.mouse.move(1,1)
        sleep(.01)
        self.mouse.move(1,1)
        sleep(.01)
        self.mouse.move(-1,-1)
        sleep(.01)
        self.mouse.move(-1,-1)
        # self.mouse.click(Button.left) # in case you want immediate drop (caution wont work as expected)


    mouse_moved_outside = False
    def handle_dnd_tui_to_gui(self, x, y): # TUI to whatever
        # print(f"TUI -> GUI X:{x} y:{y}")
        if not self.is_mouse_cursor_inside(self.get_self_geometry(),x,y):
            self.mouse_moved_outside = True


    def handle_dnd_gui_to_tui(self, x, y): # Gui to potential TUI
        # print(f"GUI -> TUI X:{x} y:{y}")
        if self.is_mouse_cursor_inside(self.get_self_geometry(),x,y) and self_window.get_attributes().map_state == 2: # 2 meaning is visible | prevents issues when you are in another i3 tab
            self.vdnd_win.move(x-5,y-5)
            self.vdnd_win.show()
        else:
            self.vdnd_win.hide()


    suppress = False
    def on_mouse_click(self, x, y, button, pressed):
        global listener
        if self.suppress: 
            self.suppress = False
            return
        if pressed and button == Button.left:
            if d.get_input_focus().focus == self_window:
                listener.on_move = self.handle_dnd_tui_to_gui
            else:
                listener.on_move = self.handle_dnd_gui_to_tui
        else:
            if self.mouse_moved_outside and listener.on_move == self.handle_dnd_tui_to_gui:
                self.mouse_moved_outside = False
                self.suppress = True
                listener.on_click = lambda *args : None # might change it to AbstractListener
                listener.on_move = lambda *args : None # might change it to AbstractListener
                self.perform_virtual_file_drag(x,y)
                listener.on_click = self.on_mouse_click # this won't work by itself, as it will "backfire" an event from self.perform_virtual_file_drag, even though we did lambda *args : None 
            listener.on_move = lambda *args : None # might change it to AbstractListener
            self.vdnd_win.hide()


    def __start_qt(self):
        app = QApplication()
        self.obj = MyObject()
        self.obj.my_signal.connect(self.dnd_slot)  # Connect the signal to a slot (a function)
        self.w   = QMainWindow()
        self.vdnd_win = DropWindow(self.__on_drop) # virtual dnd win
        QtCore.qInstallMessageHandler(qtMessageHandler) # disable almost all qt\pyside messages
        app.exec()


    # def __del__(self):
        # self.proc_qt.stop()


    def __init__(self, on_drop=lambda *args : None, on_drag=lambda *args : None):
        global listener
        listener.on_click=self.on_mouse_click
        self.__on_drop = on_drop # TODO: setter\getter
        self.__on_drag = on_drag 
        t = threading.Thread(target=self.__start_qt) # supports global
        t.daemon = True
        t.start()
        self.mouse = Controller()

