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


class ALP_RETURNCODES(Enum):
    SUCCESS = 0
    SUCC_PARTIAL = 1
    ERROR = 2147483648  # generic error, e.g. "not implemented"; should never be returned to user
    ERR_NOT_FOUND = 2147483649  # DevAlloc: serial number not found
    ERR_DUPLICATE = 2147483650  # DevAlloc: device already allocated
    ERR_INIT = 2147483651  # DevAlloc: initialization error
    ERR_RESET = 2147483652  # DevAlloc: init. error, maybe due to reset switch
    ERR_HDEVICE = 2147483653
    ERR_DISCONNECT = 2147483654
    ERR_CONNECTION = (
        2147483655  # connection error occurred, but device is (maybe) re-connected
    )
    ERR_MT = 2147483656
    ERR_HALT = 2147483657
    ERR_MEM = 2147483658
    ERR_MEM_I = 2147483659
    ERR_PARAM = 2147483660
    ERR_DONGLE = 2147483661
    ERR_API_DLL_MISSING = (
        2147483662  # The responsible API DLL could not be loaded by the ALPX wrapper.
    )
    ERR_API_DLL_UNKNOWN = 2147483663  # This ALP device version is not supported by this ALPX wrapper version.


class DlpThread(QThread):
    def __init__(self) -> None:
        super().__init__()

        self.dll: CDLL = CDLL("./alpD41.dll")

        self.alpid: ALP_ID = c_long(0)
        self.size_x: int
        self.size_y: int
        self.serial: c_long = ALP_DEFAULT

        self.connected: bool = False
        self.running: bool = False

        self.set_img_mutex: QMutex = QMutex()
        self._img: Img | None = None

        ret: ALP_RETURNCODES = self.dll.AlpDevAlloc(
            DeviceNum=c_long(self.serial.value),
            InitFlag=ALP_DEFAULT,
            ALP_ID=pointer(self.alpid),
        )
        print(ret)

        match ret:
            case ALP_RETURNCODES.SUCCESS.value:
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
