import ctypes
import os
import socket
import elevate
import app
from app.firewall.firewall import getHotspotInterfaceIndex
from app.network.lan_setup import setupLANInfrastructure, startHotspot, stopHotspot, isAdmin, resolveNameWithTimeout, \
    addLineToHostsFile, checkSetup


def testStartHotspot():
    startHotspot()
    interfaceIndex = getHotspotInterfaceIndex()
    assert interfaceIndex is not None and interfaceIndex != -1
    stopHotspot()


def testStopHotspot():
    startHotspot()
    stopHotspot()
    interfaceIndex = getHotspotInterfaceIndex()
    assert interfaceIndex is None or interfaceIndex != -1


def testIsAdmin():
    def adminIsTrue():
        return True
    ctypes.windll.shell32.IsUserAnAdmin = adminIsTrue
    assert isAdmin()

    def adminIsFalse():
        return False
    ctypes.windll.shell32.IsUserAnAdmin = adminIsFalse
    assert not isAdmin()

    def adminException():
        raise Exception

    ctypes.windll.shell32.IsUserAnAdmin = adminException
    assert not isAdmin()


def testResolveNameWithTimeout():
    def mockedGetHostByName(name):
        return '1.1.1.1'
    socket.gethostbyname = mockedGetHostByName
    result = resolveNameWithTimeout('api.lqoptics.com')
    assert result == '1.1.1.1'

    def mockedGetHostByNameException(name):
        raise Exception
    socket.gethostbyname = mockedGetHostByNameException
    result = resolveNameWithTimeout('api.lqoptics.com')
    assert result is None


def testAddLineToHostsFile(tmp_path_factory):
    def isAdminMock():
        return True
    app.network.lan_setup.isAdmin = isAdminMock

    tmp_path_factory.getbasetemp().joinpath('System32').mkdir()
    tmp_path_factory.getbasetemp().joinpath('System32').joinpath('Drivers').mkdir()
    etcTempFolderPath = tmp_path_factory.getbasetemp().joinpath('System32').joinpath('Drivers').joinpath('etc')
    etcTempFolderPath.mkdir()
    hostsFilePath = etcTempFolderPath.joinpath('hosts')
    hostsFilePath.write_text('test')

    def systemEnvMock(variableName):
        return str(tmp_path_factory.getbasetemp())

    os.getenv = systemEnvMock

    addLineToHostsFile()

    systemRootPath = os.getenv('SystemRoot')
    writtenData = open(fr'{systemRootPath}\System32\Drivers\etc\hosts', 'r').read()
    assert writtenData == 'test\n# Added by Raman management tool\n192.168.137.1 api.lqoptics.com\n# End of section\n'

    def isAdminMock():
        return False

    app.network.lan_setup.isAdmin = isAdminMock

    class ElevateMock:
        called = False

        @staticmethod
        def elevateMock(show_console):
            ElevateMock.called = True
            return

    elevate.elevate = ElevateMock.elevateMock
    addLineToHostsFile()
    assert ElevateMock.called


def testCheckSetup():

    class AddLineToHostsFileMock:
        called = False

        @staticmethod
        def addLineToHostsFile():
            AddLineToHostsFileMock.called = True
            return

    def resolveNameMock(name):
        return None
    app.network.lan_setup.resolveNameWithTimeout = resolveNameMock
    app.network.lan_setup.addLineToHostsFile = AddLineToHostsFileMock.addLineToHostsFile

    checkSetup()

    assert AddLineToHostsFileMock.called

    AddLineToHostsFileMock.called = False

    def resolveNameMock(name):
        return '1.1.1.1'
    app.network.lan_setup.resolveNameWithTimeout = resolveNameMock

    checkSetup()

    assert AddLineToHostsFileMock.called

    AddLineToHostsFileMock.called = False

    def resolveNameMock(name):
        return '192.168.137.1'
    app.network.lan_setup.resolveNameWithTimeout = resolveNameMock

    assert not AddLineToHostsFileMock.called


def testSetupLANInfrastructure():
    setupLANInfrastructure()
    interfaceIndex = getHotspotInterfaceIndex()
    assert interfaceIndex is not None and interfaceIndex != -1
    stopHotspot()
