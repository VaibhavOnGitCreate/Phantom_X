import sys
import mss
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect, QThread, pyqtSignal
from PIL import Image


SAVE_PATH = "../Phantom_X/static/capture.png"


class ScreenSelector(QWidget):

    def __init__(self):
        super().__init__()

        self.start = None
        self.end = None

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        self.setWindowState(Qt.WindowFullScreen)

        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen()
        self.background = screen.grabWindow(0)

        self.show()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background)

        if self.start and self.end:

            painter.setPen(QPen(QColor(0,255,0), 2))

            rect = QRect(self.start, self.end).normalized()

            painter.drawRect(rect)

    def mousePressEvent(self, event):

        self.start = event.pos()
        self.end = self.start

    def mouseMoveEvent(self, event):

        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):

        self.end = event.pos()

        rect = QRect(self.start, self.end).normalized()

        self.capture(rect)

        self.close()

    def capture(self, rect):

        x = rect.left()
        y = rect.top()
        w = rect.width()
        h = rect.height()

        if w <= 0 or h <= 0:
            print("Invalid selection")
            return

        with mss.mss() as sct:

            monitor = {
                "top": y,
                "left": x,
                "width": w,
                "height": h
            }

            screenshot = sct.grab(monitor)

            img = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb
            )

            img.save(SAVE_PATH)

            print("Saved:", SAVE_PATH)


# Proper main-thread launcher
def run_selector():

    app = QApplication(sys.argv)

    selector = ScreenSelector()

    app.exec_()


# Hotkey handler
def hotkey_trigger():

    print("Launching selector...")

    run_selector()


# Main listener
def start_listener():

    print("Phantom_X running...")
    print("Press CTRL + SHIFT + X")

    keyboard.add_hotkey(
        "ctrl+shift+x",
        hotkey_trigger
    )

    keyboard.wait()

