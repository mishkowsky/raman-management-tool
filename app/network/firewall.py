import re
import struct
import subprocess
import time
from threading import Thread

import elevate
import pydivert
from loguru import logger
from pydivert import Layer, Flag
from pydivert import windivert_dll
from pydivert.windivert_dll import DLL_PATH


class HotspotInterfaceIndexNotFoundException(Exception):
    pass


class Firewall:
    def __init__(self):
        self.inOutTrafficWinDivert: pydivert.WinDivert | None = None
        self.forwardTrafficWinDivert: pydivert.WinDivert | None = None
        self.stop = False

    def setupWinDivertInstances(self):
        logger.debug('INITIATING WINDIVERT INSTANCES')
        interfaceIndex = getHotspotInterfaceIndex()

        self.inOutTrafficWinDivert = pydivert.WinDivert(f"ifIdx = {interfaceIndex}", Layer.NETWORK)
        self.inOutTrafficWinDivert.register()
        self.inOutTrafficWinDivert.open()

        self.forwardTrafficWinDivert = pydivert.WinDivert(f"ifIdx = {interfaceIndex}", Layer.NETWORK_FORWARD, flags=Flag.DROP)
        self.forwardTrafficWinDivert.register()
        self.forwardTrafficWinDivert.open()

        logger.debug('INITIATION DONE')

    def getNameFromDNSRequest(self, request: bin) -> str:

        questionsCount = struct.unpack(">h", request[4:6])[0]

        if questionsCount != 1:
            return ''

        # 12:   2 for TransactionID
        #       2 for Flags
        #       2 for Questions count
        #       2 for Answer RRs
        #       2 for Authority RRs
        #       2 for Additional RRs
        # -4:   -2 for type of request
        #       -2 for class
        nameFromQuery = request[12:-4]

        nextLabelLength = nameFromQuery[0]
        name = ''
        firstIndexOfNextLabel = 1
        while nextLabelLength != 0:
            label = nameFromQuery[firstIndexOfNextLabel:firstIndexOfNextLabel + nextLabelLength].decode('utf-8')
            oldLabelLength = nextLabelLength
            nextLabelLength = nameFromQuery[firstIndexOfNextLabel + nextLabelLength]
            firstIndexOfNextLabel += oldLabelLength + 1
            if nextLabelLength != 0:
                name = f'{name}{label}.'
            else:
                name = f'{name}{label}'
        return name

    def captureInOutTraffic(self):
        logger.debug('STARTED TO CAPTURE IN/OUT TRAFFIC')
        # Of all DNS requests, only api.lqoptics.com is allowed
        for packet in self.inOutTrafficWinDivert:
            if packet.is_inbound and packet.udp is not None and packet.dst_port == 53 and packet.payload:
                try:
                    name = self.getNameFromDNSRequest(packet.payload)
                except:
                    name = ''
                if name == 'api.lqoptics.com':
                    self.inOutTrafficWinDivert.send(packet)
                    logger.debug(f'DNS FOR {name} WAS ALLOWED')
            else:
                self.inOutTrafficWinDivert.send(packet)
            if self.stop:
                logger.debug('CLOSING IN/OUT TRAFFIC')
                self.inOutTrafficWinDivert.close()
                logger.debug(f'IN/OUT TRAFFIC INSTANCE STATUS: {self.inOutTrafficWinDivert.is_open}')
                break
        logger.debug('THREAD FOR IN/OUT TRAFFIC FELL OUT FROM MAIN LOOP')

    def captureForwardTraffic(self):
        logger.debug('STARTED TO CAPTURE FORWARD TRAFFIC')
        for packet in self.forwardTrafficWinDivert:
            if self.stop:
                logger.debug('CLOSING FORWARD TRAFFIC')
                self.forwardTrafficWinDivert.close()
                logger.debug(f'FORWARD TRAFFIC INSTANCE STATUS: {self.forwardTrafficWinDivert.is_open}')
                break
        logger.debug('THREAD FOR FORWARD TRAFFIC FELL OUT FROM MAIN LOOP')

    def close(self):
        self.stop = True


def getHotspotInterfaceIndex() -> int:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    p = subprocess.run([
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "Get-NetIpAddress -IPAddress 192.168.137.1", ],
        capture_output=True, text=True, startupinfo=startupinfo)
    if p.stdout is None or p.stdout == '':
        logger.debug('HOTSPOT INTERFACE WAS NOT FOUND')
    else:
        noSpaces = re.sub(r'\s+', '', p.stdout)
        a = re.compile(r'(?<=InterfaceIndex:)\d+')
        searchRes = a.search(noSpaces)
        if searchRes:
            interfaceIndex = int(searchRes[0])
            logger.debug(f'HOTSPOT INTERFACE INDEX {interfaceIndex}')
            return interfaceIndex
        else:
            logger.debug('UNEXPECTED NO RESULT FOR REGEX')
            return -1


def runFirewallThreads(firewall: Firewall):
    logger.debug(f'WINDIVERT DLL PATH IS: {DLL_PATH}')

    firewall.setupWinDivertInstances()

    logger.debug('STARTING FORWARD TRAFFIC THREAD')
    t1 = Thread(target=firewall.captureForwardTraffic)
    t1.daemon = True
    t1.start()

    logger.debug('STARTING IN/OUT TRAFFIC THREAD')
    t2 = Thread(target=firewall.captureInOutTraffic)
    t2.daemon = True
    t2.start()
