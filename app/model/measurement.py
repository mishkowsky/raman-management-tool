import json
import re
from datetime import datetime
from pathlib import Path
import numpy as np
from numpy import average


class Measurement:
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    UI_DATETIME_FORMAT = '%H:%M:%S %d.%m.%Y'
    SPECTRUM_FREQUENCIES = [*range(200, 3203, 2)]  # [200, 202, 204, ..., 3202]

    def __init__(self):

        self.address: str = ''
        self.addressJsonString: str = ''
        self.alterType: str = ''
        self.alterTypeCode: str = ''
        self.auto: bool = False
        self.averageSpectrumValue: float = 0.0
        self.casCode: str = ''
        self.chemicalReaction: str = ''
        self.createDate: datetime = datetime.now()
        self.dangerousLevel: str = ''
        self.description: str = ''
        self.deviceType: int = 0
        self.filename: str = ''
        self.firstTitle: str = ''
        self.hsCode: str = ''
        self.hyperfluorescence: bool = False
        self.id: int = 0
        self.isWavelet: bool = False
        self.lastSelfCheckDate: datetime
        self.lastSelfCheckResult: str = ''
        self.latitude: float = 0.0
        self.longitude: float = 0.0
        self.matched: bool = False
        self.maxSpectrumList: list[float]
        self.mix: bool = False
        self.name: str = ''
        self.originalSpectrum: list = []
        self.overhaul: bool = False
        self.pngLength: int = 0
        self.remoteFileName: str
        self.safety: str
        self.samplingCount: int = 0
        self.samplingIdeaPeakValue: int = 0
        self.samplingIntegrationTime: int = 0
        self.samplingLaserLevel: int = 0
        self.samplingLaserPower: int = 0
        self.samplingLoginUserName: str = ''
        self.secondTitle: str = ''
        self.serialNumber: str = ''
        self.sgSpectrum: list = []
        self.signLength: int = 0
        self.similarity: float = 0.0
        self.slit: str = ''
        self.spectrumList: list[float] = []
        self.title: str = ''
        self.version: str = ''
        self.wlSpectrum: list = []

        self.loadedFromFilePath: str = ''

    def loadFromFile(self, filePath: str):
        with open(filePath, 'r') as file:
            fileContent = file.read()
        jsonObject = json.loads(fileContent)
        self.__dict__ = jsonObject
        listAttributes = ['spectrumList', 'maxSpectrumList', 'originalSpectrum', 'wlSpectrum']
        for listAttribute in listAttributes:
            if hasattr(self, listAttribute) and type(getattr(self, listAttribute)) is str:
                setattr(self, listAttribute, json.loads(getattr(self, listAttribute)))
        self.loadedFromFilePath = filePath
        self.createDate = datetime.strptime(jsonObject['createDate'], self.DATETIME_FORMAT)  # 1970-01-02 09:52:06
        self.averageSpectrumValue = average(self.spectrumList)
        self.name = Path(filePath).stem
        # if self.name is None and self.title is not None:
        #     self.name = self.title

    def save(self, filePath: str):
        string = json.dumps(self, indent=4, sort_keys=True, default=self.jsonSerialize)
        indent = '    '
        limit = 1
        regexPattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
        string = regexPattern.sub('', string)

        with open(filePath, 'w') as f:
            f.write(string)
            f.flush()
            f.close()

    def jsonSerialize(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, Measurement):
            attributesDoNotInclude = ['loadedFromFilePath', 'averageSpectrumValue']
            dictionary = obj.__dict__.copy()
            for attribute in attributesDoNotInclude:
                del dictionary[attribute]
            return dictionary
        if isinstance(obj, datetime):
            return obj.strftime(self.DATETIME_FORMAT)
        raise TypeError("Type %s not serializable" % type(obj))

    def normalizeAndSave(self, filePathToSave):
        normalizedSpectrum = (self.spectrumList - np.min(self.spectrumList)) / (
                    np.max(self.spectrumList) - np.min(self.spectrumList))
        normalized = Measurement()
        normalized.createDate = datetime.now()
        normalized.spectrumList = normalizedSpectrum.tolist()
        normalized.name = Path(filePathToSave).stem  # os.path.basename(filePathToSave)
        normalized.loadedFromFilePath = filePathToSave
        normalized.save(filePathToSave)

    @staticmethod
    def countAverageAndSave(ms: list['Measurement'], filePathToSave) -> 'Measurement':
        avgSpectrum = None
        resultingSpectrumLength = min(len(m.spectrumList) for m in ms)
        for m in ms:
            spectrumArray = np.array(m.spectrumList[0:resultingSpectrumLength])
            if avgSpectrum is None:
                avgSpectrum = spectrumArray
            else:
                avgSpectrum = avgSpectrum + spectrumArray
        avgSpectrum = (avgSpectrum / len(ms)).tolist()
        avg = Measurement()
        avg.spectrumList = avgSpectrum
        avg.createDate = datetime.now()
        avg.name = Path(filePathToSave).stem  # os.path.basename(filePathToSave)
        avg.loadedFromFilePath = filePathToSave
        avg.save(filePathToSave)
        return avg

    def __eq__(self, other):
        if isinstance(other, Measurement):
            return self.loadedFromFilePath == other.loadedFromFilePath
        return False

    def __hash__(self):
        return hash(self.loadedFromFilePath)
