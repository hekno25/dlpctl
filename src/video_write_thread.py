from PySide6.QtCore import QThread, Slot


class VideoWriteThread(QThread):
    def run(self):
        self.exec_()

    @Slot(tuple)
    def save_frame(self, frame_out):
        frame, out = frame_out
        if out is not None and frame is not None:
            try:
                out.write(frame)
            except Exception as e:
                print(f"Error reading frame from camera thread: {e}")
