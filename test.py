#!/usr/bin/env python3
import ctypes
import ctypes.util
import os
import errno

libc = ctypes.CDLL("libc.so.6", use_errno=True)

class UsbCtrlTransfer(ctypes.Structure):
    _fields_ = [
        ("bRequestType", ctypes.c_uint8),
        ("bRequest",     ctypes.c_uint8),
        ("wValue",       ctypes.c_uint16),
        ("wIndex",       ctypes.c_uint16),
        ("wLength",      ctypes.c_uint16),
        ("timeout",      ctypes.c_uint32),
        ("data",         ctypes.c_void_p),
    ]

data = (ctypes.c_uint8 * 3)(0x80, 0xBB, 0x00)

req = UsbCtrlTransfer(
    bRequestType = 0x22,
    bRequest     = 0x01,
    wValue       = 0x0100,
    wIndex       = 0x0102,
    wLength      = 3,
    timeout      = 1000,
    data         = ctypes.addressof(data),
)

USBDEVFS_CONTROL = 0xC0185500

fd = os.open('/dev/bus/usb/001/020', os.O_RDWR)
ret = libc.ioctl(fd, USBDEVFS_CONTROL, ctypes.byref(req))
err = ctypes.get_errno()
print(f"ioctl returned: {ret}")
print(f"errno: {err} ({errno.errorcode.get(err, 'unknown')})")
os.close(fd)
