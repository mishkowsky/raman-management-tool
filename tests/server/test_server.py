import os
import pytest
from app.server import server
from app.server.server import serverApp, getJsonStringFromBinaryRequest


@pytest.fixture()
def app():
    serverApp.config.update({
        "TESTING": True,
    })
    yield serverApp


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def testUploadHistory(tmp_path_factory, client):
    server.uploadFolder = str(tmp_path_factory.getbasetemp())

    # Original request from raman, including unexpected data
    data = b'\x00\x00\xd2u{' \
           b'"addressJsonString":"{}",' \
           b'"alterType":"No match",' \
           b'"alterTypeCode":"No match",' \
           b'"auto":false,' \
           b'"casCode":"No match",' \
           b'"chemicalReaction":"No match",' \
           b'"createDate":"1970-01-06 06:06:27",' \
           b'"dangerousLevel":"No match",' \
           b'"description":"No match ThermoResist: 1.92",' \
           b'"deviceType":0,' \
           b'"filename":"",' \
           b'"firstTitle":"Handheld Raman",' \
           b'"hsCode":"No match",' \
           b'"hyperfluorescence":false,' \
           b'"id":820,' \
           b'"isWavelet":true,' \
           b'"lastSelfCheckDate":"1970-01-06 05:23:55",' \
           b'"lastSelfCheckResult":"\xe6\x88\x90\xe5\x8a\x9f",' \
           b'"latitude":59.742516,' \
           b'"longitude":30.433952,' \
           b'"matched":false,' \
           b'"maxSpectrumList":"[211.18, 244.84, 280.38]",' \
           b'"mix":true,' \
           b'"name":"No match",' \
           b'"originalSpectrum":"[37501.16050583664, 37698.084859854, 37663.30926208201]",' \
           b'"overhaul":false,' \
           b'"pngLength":0,' \
           b'"remoteFileName":"425198289__report_form.pdf",' \
           b'"safety":"Unknown",' \
           b'"samplingCount":6,' \
           b'"samplingIdeaPeakValue":38,' \
           b'"samplingIntegrationTime":500,' \
           b'"samplingLaserLevel":200,' \
           b'"samplingLaserPower":200,' \
           b'"samplingLoginUserName":"admin",' \
           b'"secondTitle":"RAMAN",' \
           b'"serialNumber":"B7BP221202",' \
           b'"sgSpectrum":"[]",' \
           b'"signLength":0,' \
           b'"similarity":0.0,' \
           b'"slit":"SLIT25",' \
           b'"spectrumList":"[211.18, 244.84, 383.07]",' \
           b'"version":"V4.1Rev48",' \
           b'"wlSpectrum":"[]"' \
           b'}3.4, 103.08, 103.09, 103.42, 104.01, 104.84, 105.86, 107.03, ' \
           b'108.3, 109.64, 110.98, 112.3, 113.55, 114.69, 115.7, 116.54, 117.18, 117.62, 117.83, 117.8, 117.54, ' \
           b'117.05, 116.34, 115.43, 114.33, 113.07, 111.67, 110.17, 108.6, 106.99, 105.38, 103.8, 102.27, 100.84, ' \
           b'99.53, 98.35, 97.34, 96.51, 95.86, 95.41, 95.15, 95.08, 95.2, 95.49, 95.93, 96.5, 97.19, 97.96, 98.8, ' \
           b'99.67, 100.56, 101.43, 102'

    response = client.post('/UpLoadFileService.svc/web/CreateUploadHistory', data=data)
    assert response.status_code == 200
    expectedJsonObject = {
        "message": "上传成功",
        "obj": "my_link.com",
        "success": True}
    assert response.json == expectedJsonObject
    assert os.path.exists(tmp_path_factory.getbasetemp().joinpath('No match.txt'))

    response = client.post('/UpLoadFileService.svc/web/CreateUploadHistory', data=data)
    assert os.path.exists(tmp_path_factory.getbasetemp().joinpath('No match (1).txt'))

    data = b'{"name": "", "title": ""}'
    response = client.post('/UpLoadFileService.svc/web/CreateUploadHistory', data=data)
    assert response.status_code == 200
    assert os.path.exists(tmp_path_factory.getbasetemp().joinpath('Untitled.txt'))

    data = b''
    response = client.post('/UpLoadFileService.svc/web/CreateUploadHistory', data=data)
    assert response.status_code == 422


def testGetJsonStringFromBinaryRequest():
    assert getJsonStringFromBinaryRequest(b'') == ''


def testDevices(client):
    response = client.get('/BaseInfoService.svc/web/Devices/9067665c1bae90757c7259eff16bfcb2')
    expectedJsonObject = {"message": "请求成功", "obj": "", "success": True}
    assert response.status_code == 200
    assert response.json == expectedJsonObject


def testCreateLoginMessage(client):
    data = {
        "address": "RussiaSaint Petersburgшоссе Подбельского",
        "apkVersionName": "V4.1Rev48",
        "electricity": "88%",
        "iccid": "",
        "latitude": 59.737001,
        "loginUser": "admin",
        "longitude": 30.427566,
        "power": 200.0,
        "serialNumber": "B7BP221202",
        "status": "开机"
    }
    response = client.post('/Service1.svc/web/CreateLoginMessage', json=data)
    expectedJsonResponseObject = {"MId": "b718a0f0-aa26-4b35-b266-170b3e4e509c", "Success": True, "UserSn": ""}
    assert response.status_code == 200
    assert response.json == expectedJsonResponseObject


def testGetLockTypes(client):
    response = client.post('/BaseInfoService.svc/web/GetLockTypes', data='')
    expectedJsonObject = [{"code": 1, "regularcode": "100"},
                          {"code": 2, "regularcode": "011"},
                          {"code": 3, "regularcode": "111"}]
    assert response.status_code == 200
    assert response.json == expectedJsonObject


def testGetDeviceLockStatus(client):
    response = client.post('/BaseInfoService.svc/web/GetDeviceLockStatus', data='9067665c1bae90757c7259eff16bfcb2')
    expectedJsonObject = {"message": "请求成功",
                          "obj": {"code": 0, "duration": 0, "expiredDate": 0, "name": "不锁定"},
                          "success": True}
    assert response.status_code == 200
    assert response.json == expectedJsonObject


def testModifyLoginMessage(client):
    response = client.post('/Service1.svc/web/ModifyLoginMessage', data='b718a0f0-aa26-4b35-b266-170b3e4e509c')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == '成功'
