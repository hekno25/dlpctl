import time
import numpy as np
from PySide6.QtCore import QThread, Signal
from pypylon import pylon
from pypylon.pylon import GrabResult, InstantCamera, RuntimeException
import cv2


class CameraThread(QThread):
    """
    A `QThread` based class for handling a Basler camera connection and its operations
    """

    timestamp = Signal(float)
    display_out = Signal(tuple)
    frame_out = Signal(tuple)

    def __init__(self, desired_fps=100) -> None:
        super().__init__()
        self.recording: bool = False

        # If `None`, there is no video writer
        self.out: cv2.VideoWriter | None = None

        self.desired_fps = desired_fps

        # If `None`, there is no Basler connection
        self.basler: InstantCamera | None = None
        self.running = False

    def start_grabbing(self) -> None:
        """
        Starts the Basler camera's continuous frame grabbing
        """
        if self.basler:
            self.basler.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def stop_grabbing(self) -> None:
        """
        Stops the Basler camera from grabbing new frames
        """
        if self.basler:
            self.basler.StopGrabbing()

    def start_recording(self) -> None:
        """
        Starts recording and opens the video writer
        """
        print("starting capture")
        self.start_time = time.time()
        if self.basler:
            fourcc = cv2.VideoWriter.fourcc(*"mp4v")
            output_filename = "unfiltered_output.mp4"
            self.out = cv2.VideoWriter(
                output_filename,
                fourcc,
                30,
                (1280, 1024),
                isColor=False,
            )
        self.recording = True

    def stop_recording(self) -> None:
        """
        Stops recording and saves the video
        """
        self.recording = False
        if self.out:
            self.out.release()
            self.out = None
            self.wait()

    def run(self) -> None:
        previous_frame = None
        accumulator = 0
        acc_ratio = 30 / self.desired_fps
        self.running = True

        if self.basler:
            while self.basler.IsGrabbing():

                if self.running == False:
                    break

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
                            self.frame_out.emit([frame, self.out])
                        except Exception as e:
                            print(f"Error emitting write frame: {e}")
                        self.timestamp.emit(time.time() - self.start_time)

                    if accumulator >= 1.0:
                        try:
                            exposure = self.basler.ExposureTime.Value
                            current_fps = self.basler.ResultingFrameRate.Value
                            self.display_out.emit(
                                [frame, current_fps, exposure, self.recording]
                            )
                        except Exception as e:
                            print(f"Error emitting display frame: {e}")
                        accumulator -= 1.0

    def handle_framerate(self) -> None:
        """
        This method checks if the current FPS is the target FPS.
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

    def open(self) -> bool:
        """
        Opens a connection to a Basler camera

        Returns `True` if connection succeeded and `False` if not
        """

        try:
            self.basler = pylon.InstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice()
            )

            print("Using Basler Camera: ", self.basler.GetDeviceInfo().GetModelName())
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
            return True
        except RuntimeException:
            self.basler = None
            return False

    def set_exposure(self, value: int) -> None:
        if self.basler:
            old_exposure = self.exposure
            try:
                self.exposure = value
                self.basler.ExposureTime.Value = self.exposure
            except RuntimeException as e:
                print("RuntimeException from pylon: {e}")
                self.exposure = old_exposure

    def close(self) -> None:
        """
        Close connection to Basler camera
        """
        if self.basler:
            self.basler.Close()
            self.basler = None

    def stop(self):
        self.stop_grabbing()
        self.running = False
        self.quit()