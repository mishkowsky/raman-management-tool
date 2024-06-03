import json
import os
import re
from json import JSONDecodeError
from flask import Flask, Response
from flask import request
from loguru import logger

serverApp = Flask(__name__)
uploadFolder = 'C:/'


@serverApp.route('/UpLoadFileService.svc/web/CreateUploadHistory', methods=['POST'])
def uploadHistory():
    hex_bytes = request.data

    jsonString = getJsonStringFromBinaryRequest(hex_bytes)

    try:
        data = json.loads(jsonString)
    except JSONDecodeError:
        return Response("{'error': 'unprocessable entity'}", status=422, mimetype='application/json')

    listAttributes = ['spectrumList', 'maxSpectrumList', 'originalSpectrum', 'wlSpectrum']
    for listAttribute in listAttributes:
        if listAttribute in data.keys() and type(data[listAttribute]) is str:
            data[listAttribute] = json.loads(data[listAttribute])

    text = json.dumps(data, indent=4, sort_keys=True)
    text = jsonIndentLimit(text, '    ', 1)

    name = data['name']
    if name is None or name == '':
        name = data['title']
    if name is None or name == '':
        name = 'Untitled'
    name.replace('/', '_')
    name.replace('\\', '_')
    filePath = f'{uploadFolder}/{name}.txt'
    i = 0
    while os.path.exists(filePath):
        i += 1
        filePath = f'{uploadFolder}/{name} ({i}).txt'
    with open(filePath, 'w') as file:
        file.write(text)
        file.flush()
        file.close()

    return {'message': '上传成功', 'obj': 'my_link.com', 'success': True}


def getJsonStringFromBinaryRequest(data: bytes) -> str:
    openingBracketCounter = 0
    closingBracketCounter = 0
    index = 0
    firstOpeningBracketIndex = -1
    lastClosingBracketIndex = -1
    for byte in data:
        char = chr(byte)
        if char == '{':
            if openingBracketCounter == 0:
                firstOpeningBracketIndex = index
            openingBracketCounter += 1
        elif char == '}':
            closingBracketCounter += 1
            if closingBracketCounter == openingBracketCounter:
                lastClosingBracketIndex = index
        index += 1
    if firstOpeningBracketIndex == -1 or lastClosingBracketIndex == -1:
        return ''
    return data[firstOpeningBracketIndex:lastClosingBracketIndex + 1].decode('utf-8')


def jsonIndentLimit(jsonString, indent, limit):
    regexPattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
    return regexPattern.sub('', jsonString)


# GET /BaseInfoService.svc/web/Devices/9067665c1bae90757c7259eff16bfcb2
@serverApp.route('/BaseInfoService.svc/web/Devices/<deviceCode>', methods=['GET'])
def devices(deviceCode):
    binary = request.data
    logger.debug(len(binary))
    logger.debug(deviceCode)
    return {'message': '请求成功', 'obj': '', 'success': True}


@serverApp.route('/Service1.svc/web/CreateLoginMessage', methods=['POST'])
def createLoginMessage():
    binary = request.data
    logger.debug(len(binary))
    return {'MId': 'b718a0f0-aa26-4b35-b266-170b3e4e509c', 'Success': True, 'UserSn': ''}


@serverApp.route('/BaseInfoService.svc/web/GetLockTypes', methods=['POST'])
def getLockTypes():
    binary = request.data
    logger.debug(len(binary))
    return [{'code': 1, 'regularcode': '100'}, {'code': 2, 'regularcode': "011"}, {'code': 3, 'regularcode': '111'}]


@serverApp.route('/BaseInfoService.svc/web/GetDeviceLockStatus', methods=['POST'])
def getDeviceLockStatus():
    binary = request.data
    logger.debug(len(binary))
    return {
        'message': '请求成功',  # Запрос успешен
        'obj': {
            'code': 0,
            'duration': 0,
            'expiredDate': 0,
            'name': '不锁定'  # Не заблокировано
        },
        'success': True
    }


@serverApp.route('/Service1.svc/web/ModifyLoginMessage', methods=['POST'])
def modifyLoginMessage():
    binary = request.data
    logger.debug(len(binary))
    return '成功'  # Успех
