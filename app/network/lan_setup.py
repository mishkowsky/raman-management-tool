import ctypes
import os
import socket
import subprocess
import time
from threading import Thread
from time import sleep
import elevate
from icmplib import ping
from loguru import logger


def getHotspotScript(value: int):
    """
    :param value: 0 for disable, 1 for enable
    """
    return f"""

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }})[0]

Function Await($WinRtTask, $ResultType) {{
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}}

Function AwaitAction($WinRtAction) {{
    $asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and !$_.IsGenericMethod }})[0]
    $netTask = $asTask.Invoke($null, @($WinRtAction))
    $netTask.Wait(-1) | Out-Null
}}

Function SetHotspot($Enable) {{
    $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
    $tetheringManager = [Windows.Networking.NetworkOperators.NetworkOperatorTetheringManager,Windows.Networking.NetworkOperators,ContentType=WindowsRuntime]::CreateFromConnectionProfile($connectionProfile)
    Write-Output $$connectionProfile
    if ($Enable -eq 1) {{
        if ($tetheringManager.TetheringOperationalState -eq 1)
        {{
            "Hotspot is already On!"
        }}
        else{{
            "Hotspot is off! Turning it on"
            Await ($tetheringManager.StartTetheringAsync()) ([Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult])
        }}
    }}
    else {{
        if ($tetheringManager.TetheringOperationalState -eq 0)
        {{
            "Hotspot is already Off!"
        }}
        else{{
            "Hotspot is on! Turning it off"
            Await ($tetheringManager.StopTetheringAsync()) ([Windows.Networking.NetworkOperators.NetworkOperatorTetheringOperationResult])
        }}
    }}
}}

SetHotspot({value})

"""


def setupLANInfrastructure():
    startHotspot()
    sleep(0.25)
    checkSetup()


def startHotspot():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen([
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        getHotspotScript(1)], startupinfo=startupinfo).wait()


def stopHotspot():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen([
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        getHotspotScript(0)], startupinfo=startupinfo)


def resolveNameWithTimeout(nameToResolve, timeout=1) -> str | None:
    res = {'address': None}

    def _resolveName(name, res_):
        try:
            res_['address'] = socket.gethostbyname(name)
            logger.debug(f'RES.ADDRESS IS SET AS {res_["address"]}')
        except:
            logger.debug('DNS RESOLVE ERROR')
            pass

    timeThread = Thread(target=time.sleep, args=(timeout,))
    timeThread.daemon = True
    DNSThread = Thread(target=_resolveName,  kwargs={"name": nameToResolve, "res_": res})
    DNSThread.daemon = True

    timeThread.start()
    DNSThread.start()

    logger.debug(f'TIME THREAD IS ALIVE: {timeThread.is_alive()}')
    logger.debug(f'DNS THREAD IS ALIVE: {DNSThread.is_alive()}')

    while timeThread.is_alive():
        if not DNSThread.is_alive():
            break

    logger.debug(f'TIME THREAD IS ALIVE: {timeThread.is_alive()}')
    logger.debug(f'DNS THREAD IS ALIVE: {DNSThread.is_alive()}')
    logger.debug(f'RETURNING {res["address"]}')
    return res['address']


def checkSetup():
    targetName = 'api.lqoptics.com'
    address = resolveNameWithTimeout(targetName)
    logger.debug(f'RESOLVED ADDRESS {address}')
    if address is None:
        addLineToHostsFile()
        logger.debug(f'DNS IS UNAVAILABLE (PROBABLY WE ARE OFFLINE AND THERE NO ENTRY IN HOSTS FILE)')
        return
    if address != '192.168.137.1':
        addLineToHostsFile()
        logger.debug(f'DNS RESOLVED INTO UNEXPECTED ADDRESS')
        return

    res = ping(address, count=3, timeout=0.5, interval=0.25)
    if not res.is_alive:
        logger.debug('HOTSPOT WAS NOT STARTED FOR SOME REASONS')


def isAdmin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def addLineToHostsFile():
    if not isAdmin():
        elevate.elevate(show_console=False)
    systemRootPath = os.getenv('SystemRoot')
    with open(fr'{systemRootPath}\System32\Drivers\etc\hosts', 'a') as file:
        file.write('\n# Added by Raman management tool'
                   '\n192.168.137.1 api.lqoptics.com'
                   '\n# End of section\n')
        file.flush()
