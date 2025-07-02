import time
import numpy as np
from PySide6.QtCore import QThread, Signal
from pypylon import pylon
from pypylon.pylon import GrabResult, InstantCamera, RuntimeException
import cv2

from exception import DlpctlException


class Camera(QThread):
    timestamp = Signal(float)
    display_out = Signal(tuple)
    frame_out = Signal(tuple)

    def __init__(self, desired_fps=100) -> None:
        super().__init__()
        self.recording: bool = False
        self.out: cv2.VideoWriter | None = None

        self.desired_fps = desired_fps

        try:
            self.basler: InstantCamera | None = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice()
            )

            if self.basler:
                print(
                    "Using Basler Camera: ", self.basler.GetDeviceInfo().GetModelName()
                )
                self.basler.Open()
                self.basler.PixelFormat.Value = "Mono8"
                self.basler.ExposureAuto.Value = "Off"
                self.basler.Gain.Value = 0

                self.MAX_EXPOSURE = 20000
                self.MIN_EXPOSURE = 100
                self.exposure = 1000
                self.basler.ExposureTime.Value = self.exposure

                self.basler.AcquisitionFrameRateEnable.SetValue(False)
                self.basler.AcquisitionFrameRate.SetValue(self.desired_fps)

                self.converter = pylon.ImageFormatConverter()
                self.converter.OutputPixelFormat = pylon.PixelType_Mono8
                self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
                self.start_grabbing()
        except RuntimeException as e:
            self.basler = None
            raise DlpctlException(e)

    def start_grabbing(self) -> None:
        """
        Continuously grab the latest image in the background
        """
        if self.basler:
            self.basler.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_grabbing(self) -> None:
        if self.basler:
            self.basler.StopGrabbing()

    def start_recording(self):
        print("recording")
        self.start_time = time.time()
        if self.basler:
            fourcc = cv2.VideoWriter.fourcc(*"mp4v")
            output_filename = "output.mp4"
            self.out = cv2.VideoWriter(
                output_filename,
                fourcc,
                30,
                (1280, 1024),
                isColor=False,
            )
        self.recording = True

    def stop_recording(self):
        self.recording = False
        if self.out:
            self.out.release()
            self.out = None

    def run(self) -> None:
        previous_frame = None
        accumulator = 0
        acc_ratio = 30 / self.desired_fps

        if self.basler:
            while self.basler.IsGrabbing():
                grab_result: GrabResult = self.basler.RetrieveResult(
                    5000, pylon.TimeoutHandling_ThrowException
                )
                if grab_result.GrabSucceeded():
                    accumulator += acc_ratio

                    img = self.converter.Convert(grab_result)
                    frame = img.GetArray()

                    if previous_frame is None:
                        previous_frame = frame.copy()

                    self.handle_framerate()

                    if frame is None or frame.size == 0:
                        print("Invalid frame received! Passing previous frame.")
                        frame = previous_frame
                    else:
                        previous_frame = frame.copy()

                    if self.recording and self.out and self.out.isOpened():
                        try:
                            self.frame_out.emit((frame, self.out))
                        except Exception as e:
                            print(f"Error emitting write frame: {e}")
                        self.timestamp.emit(time.time() - self.start_time)

                    if accumulator >= 1.0:
                        try:
                            exposure = self.basler.ExposureTime.Value
                            current_fps = self.basler.ResultingFrameRate.Value
                            self.display_out.emit(
                                (frame, current_fps, exposure, self.recording)
                            )
                        except Exception as e:
                            print(f"Error emitting display frame: {e}")
                        accumulator -= 1.0

    def handle_framerate(self) -> None:
        """
        This method basically checks if the current FPS is the target FPS.
        If the current FPS is too low, it will disable `AcquisitionFrameRateEnable`
        mode temporarily in order to adjust the exposure accordingly.
        """
        if self.basler is None:
            return

        current_fps = self.basler.ResultingFrameRate.Value
        if current_fps < self.desired_fps:
            # Temporarily disable aquisition framerate mode
            self.basler.AcquisitionFrameRateEnable.SetValue(False)
            self.exposure = self.basler.ExposureTime.Value
            diff = np.abs(current_fps - self.desired_fps - 1)
            step = diff / 2
            if current_fps < self.desired_fps and self.exposure > self.MIN_EXPOSURE:
                self.basler.ExposureTime.Value -= step
            elif current_fps > self.desired_fps and self.exposure < self.MAX_EXPOSURE:
                self.basler.ExposureTime.Value += step
        else:
            self.basler.AcquisitionFrameRateEnable.SetValue(True)
            self.basler.AcquisitionFrameRate.SetValue(self.desired_fps)

    def __del__(self) -> None:
        if self.basler:
            self.basler.Close()
