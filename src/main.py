from PySide6.QtCore import QTimer
import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import QLabel, QMainWindow

from ui.ui_dlpctl import Ui_MainWindow

from camera import Camera
from video_write_thread import VideoWriteThread
import video_write_thread

if sys.platform == "win32":
    from dlp import DLP
else:
    from dlp import MockDLP as DLP

from exception import DlpctlException


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("DLP Control")

        self.camera: Camera | None = None
        self.pushButton.clicked.connect(self.connect_camera)

        self.video_write_thread: VideoWriteThread = VideoWriteThread()

        self.dlp: DLP | None = None
        self.pushButton_2.clicked.connect(self.connect_dlp)

        self.capture.setEnabled(False)
        self.capture.pressed.connect(self.on_capture)

    def connect_camera(self):
        if self.camera is None:
            try:
                self.camera = Camera()
                self.camera.start()
                self.capture.setEnabled(True)
                self.pushButton.setStyleSheet("color: green;")
                self.camera.frame_out.connect(self.video_write_thread.save_frame)
                self.camera.display_out.connect(self.update_display)
            except DlpctlException as e:
                self.camera = None
                self.capture.setEnabled(False)
                print(f"Could not open camera: {e}")
        else:
            self.camera = None
            self.capture.setEnabled(False)
            self.pushButton.setStyleSheet("")

    def connect_dlp(self):
        if self.dlp is None:
            try:
                self.dlp = DLP()
                self.pushButton_2.setStyleSheet("color: green;")
            except DlpctlException as e:
                print(e)
                self.dlp = None
        else:
            self.dlp = None
            self.pushButton_2.setStyleSheet("")

    def on_capture(self):
        if self.camera and not self.camera.recording:
            print("starting capture")
            self.capture.setStyleSheet("color: green;")
            self.camera.start_recording()
        elif self.camera and self.camera.recording:
            self.camera.stop_recording()
            self.capture.setStyleSheet("")
            print("stopping capture, saved to output.mp4")

    def closeEvent(self, _):
        if self.camera:
            self.camera.stop_recording()
            self.camera.wait()

    def update_display(self, data):
        print("updating display")
        if self.camera:
            frame, current_fps, exposure, recording_state = data
            h, w = frame.shape
            channels = 1
            q_img = QImage(
                frame.data, w, h, channels * w, QImage.Format.Format_Grayscale8
            )
            pixmap = QPixmap.fromImage(q_img)
            self.video_frame.setPixmap(pixmap)


if __name__ == "__main__":
    app = None
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    window = MainWindow()

    window.show()
    if app:
        app.exec()
