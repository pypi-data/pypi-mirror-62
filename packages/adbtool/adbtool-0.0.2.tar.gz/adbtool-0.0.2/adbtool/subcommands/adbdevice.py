import argparse
import sys
from typing import List

from ..cmd import call, getAdb
from ..config import Config


class Device:
    """docstring for Device"""

    __slots__ = ("serial", "online", "product", "model", "device", "raw")

    def __init__(self, line:str):
        self.raw = line
        arr = line.split()
        self.serial = arr[0]
        self.online = arr[1] == "device"
        self.product = arr[2].replace("product:", "")
        self.model = arr[3].replace("model:", "")
        self.device = arr[4].replace("device:", "")


def listOneItem(arr, index):
    if 0 < index <= len(arr):
        return arr[index - 1]
    return None

def get_devices()->List[Device]:
    output, isOk = call("%s devices -l" % getAdb())
    devices:List[Device] = []
    if isOk:
        output = output.replace("\r\n", "\n").strip()
        lines = output.split("\n")
        if len(lines) > 1:
            # skip first line "List of devices attached"
            for line in lines[1:]:
                if len(line) > 0:
                    devices.append(Device(line))
    devices.sort(key=lambda x: x.serial.lower())
    return devices


def getDevicesBySerial(devices, serial):
    serial = serial.lower()
    return list(
        filter(lambda device: device.serial.lower().startswith(serial), devices)
    )


# return
#   None: 1. no devices connected
#         2. filter can not match unique device
#         3. not filter but has more than devices
#   Empty List: can not match devices
#   List: matched devices
def filterDevices(devices, args):
    if len(devices) == 0:
        print("No devices connected")
        return None

    if args is None:
        if len(devices) == 1:
            return devices
        print("devices count:%d  please set devices command" % len(devices))
        return None

    selects = []
    for arg in args:
        device = None
        if len(arg) == 1:
            if arg == "a":
                return devices
            device = listOneItem(devices, int(arg))
        elif len(arg) >= 2:
            tmp = getDevicesBySerial(devices, arg)
            if len(tmp) == 1:
                device = tmp[0]
            elif len(tmp) > 1:
                print("serial prefix %s is not unique" % arg)
                return None
        if device is not None:
            selects.append(device)
    return selects if len(selects) > 0 else None


def printDevices(devices):
    if devices is None:
        return
    for i in range(len(devices)):
        print("%-3d %s" % (i + 1, devices[i].raw))


##### for other script
def getSerials(devices):
    if devices is not None:
        serials = []
        for d in devices:
            serials.append(d.serial)
        return serials
    return None


def addArgumentParser(parser):
    parser.add_argument(
        "-d",
        "--devices",
        nargs="*",
        help="""filter of devices, [a | n | serial]
            a: all devices
            n: index of devices list(start with 1)
            serial: devices serial (at least 2 char)
            not argument is show device list""",
    )


def doArgumentParser(args):
    devices = get_devices()
    if args.devices is not None and len(args.devices) == 0:
        printDevices(devices)
        return (True, None)

    devices = filterDevices(devices, args.devices)
    serials = getSerials(devices)
    return (False, serials, devices)


def docommand(args: argparse.Namespace, cfg: Config) -> None:
    if args.list:
        printDevices(get_devices())
        exit(0)

    devices = filterDevices(get_devices(), args.devices)
    printDevices(devices)


##### end for other script
# -------------- main ----------------
def addcommand(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-d",
        "--devices",
        nargs="+",
        help="filter of devices, [n | serial | a] n:index of list(start with 1), serial:at least 2 char, a:all",
    )
    parser.add_argument("-l", "--list", action="store_true", help="show devices list")
