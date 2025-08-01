from enum import Enum
from typing import Any, TypeAlias, override
import numpy as np
from ctypes import CDLL, c_long, c_ulong, pointer
from PySide6.QtCore import QMutex, QMutexLocker, QThread

Img: TypeAlias = np.ndarray[tuple[int, int, int], np.dtype[np.uint8]]

ALP_ID: TypeAlias = c_long

ALP_DEFAULT: c_long = c_long(0)


class ALPB_DMDTYPES(Enum):
    INVALID = 0
    XGA = 1
    SXGA_PLUS = 2
    FHD1080P_095A = 3  # (1080P 0.95" Type A)
    XGA_07A = 4  # (XGA .7" Type A)
    XGA_055A = 5  # (XGA .55" Type A)
    XGA_055X = 6  # (XGA .55" Type X)
    WUXGA_096A = 7  # (WUXGA 0.96" Type A)
    WXGA_S450 = 8  # (WXGA 0.65" s450)

    DISCONNECT = (
        255,
    )  # DMD type not recognized or no DMD connected, this behaves like 1080p by default


class Result(Enum):
    ALP_OK = 0x00000000
    ALP_NOT_ONLINE = 1001
    ALP_NOT_IDLE = 1002
    ALP_NOT_AVAILABLE = 1003
    ALP_NOT_READY = 1004
    ALP_PARM_INVALID = 1005
    ALP_ADDR_INVALID = 1006
    ALP_MEMORY_FULL = 1007
    ALP_SEQ_IN_USE = 1008
    ALP_HALTED = 1009
    ALP_ERROR_INIT = 1010
    ALP_ERROR_COMM = 1011
    ALP_DEVICE_REMOVED = 1012
    ALP_NOT_CONFIGURED = 1013
    ALP_LOADER_VERSION = 1014
    ALP_ERROR_POWER_DOWN = 1018


class DlpThread(QThread):
    def __init__(self) -> None:
        super().__init__()

        self.dll: CDLL = CDLL("./alpD41.dll")

        self.alpid: ALP_ID = ALP_DEFAULT
        self.size_x: int
        self.size_y: int
        self.serial: c_long = ALP_DEFAULT

        self.connected: bool = False
        self.running: bool = False

        self.set_img_mutex: QMutex = QMutex()
        self._img: Img | None = None

        ret: Result = self.dll.AlpDevAlloc(
            DeviceNum=c_long(self.serial.value),
            InitFlag=ALP_DEFAULT,
            ALP_ID=pointer(self.alpid),
        )
        print(ret)

        match ret:
            case Result.ALP_OK.value:
                print("Allocated ALP successfully")
            case _:
                print(f"Problem allocating ALP, return code: {ret}")

    @override
    def run(self) -> None:
        pass
        if self.img is not None and not self.running:
            pass

    def open(self) -> bool:
        """
        Open connection to DLP
        """
        if not self.connected:
            self.connected = True
            return True
        else:
            self.connected = False
            return False

    @property
    def img(self) -> Img | None:
        return self._img

    @img.setter
    def img(self, new_img: Img | None) -> None:
        """
        Push a new image sequence to the DLP
        """
        if new_img is None:
            self._img = None
        else:
            with QMutexLocker(self.set_img_mutex):
                if self.validate_img(new_img):
                    # Pause and get rid of old sequence if already allocated
                    if self.img:
                        self._img = None
                        # self.device.Halt()
                        # self.device.FreeSeq()

                    # Allocate and push new sequence data
                    # self.device.SeqAlloc(nbImg=1, bitDepth=1)
                    padded_seq = self.pad_img_centered(new_img)
                    # self.device.SeqPut(padded_seq)
                    self._img = padded_seq

    def pad_img_centered(self, img: Img) -> Img:
        target_x = self.size_x
        target_y = self.size_y

        actual_x = img.shape[0]
        actual_y = img.shape[1]

        pad_rows = (target_y - actual_y) // 2
        pad_cols = (target_x - actual_x) // 2

        print(f"nSizeX: {self.size_x}")
        print(f"nSizeY: {self.size_y}")
        print(f"pad_rows: {pad_rows}")
        print(f"pad_cols: {pad_cols}")

        padded_img = np.pad(
            array=img,
            pad_width=((pad_cols, pad_cols), (pad_rows, pad_rows)),
            mode="constant",
            constant_values=0,
        )
        return padded_img

    def validate_img(self, img: Img) -> bool:
        """
        Returns True if img is a valid image for the DLP to allocate/use
        """
        return img.shape <= (self.size_x, self.size_y)

    def close(self) -> None:
        # self.device.Halt()
        # self.device.FreeSeq()
        # self.device.Free()
        pass

    def stop(self) -> None:
        self.quit()

    def __del__(self) -> None:
        self.close()
