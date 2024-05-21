from app.model.measurement import Measurement

TEST_MEASUREMENTS = [
    '''{
        "createDate": "2024-02-11 15:21:28",
        "name": "test_1",
        "spectrumList": [
            1.0,
            1.0,
            1.0
        ]
    }''',
    '''{
        "createDate": "2024-02-11 15:21:28",
        "name": "test_2",
        "spectrumList": [
            2.0,
            2.0,
            2.0
        ]
    }''',
]


class TestMeasurement:

    # def testInit(self):
    #     m = Measurement()

    def testLoadFromFile(self, tmp_path_factory):
        tmp_file_path = tmp_path_factory.getbasetemp().joinpath(f"test_1.txt")
        tmp_file_path.write_text(TEST_MEASUREMENTS[0])
        m = Measurement()
        m.loadFromFile(str(tmp_file_path))
        assert m.loadedFromFilePath == str(tmp_file_path)
        assert m.spectrumList == [1.0, 1.0, 1.0]

    def testSave(self, tmp_path_factory):
        testSpectrum = [0, 1]

        tmp_file_path = str(tmp_path_factory.getbasetemp().joinpath(f"test_1.txt"))
        m = Measurement()
        m.spectrumList = testSpectrum
        m.save(tmp_file_path)

        m1 = Measurement()
        m1.loadFromFile(tmp_file_path)
        assert m1.spectrumList == testSpectrum

    # def testJsonSerialize(self):
    #     m = Measurement()
    #     m.spectrumList = [1, 2, 3]
    #     jsonDictionary = m.jsonSerialize()

    def testNormalizeAndSave(self, tmp_path_factory):
        tmp_file_path = str(tmp_path_factory.getbasetemp().joinpath(f"normalized.txt"))
        m = Measurement()
        m.spectrumList = [0, 1, 2]
        m.normalizeAndSave(tmp_file_path)
        normalized = Measurement()
        normalized.loadFromFile(tmp_file_path)
        assert normalized.spectrumList == [0, 0.5, 1]

    def testCountAverageAndSave(self, tmp_path_factory):
        m1 = Measurement()
        m2 = Measurement()
        m1.spectrumList = [0, 1, 2]
        m2.spectrumList = [2, 1, 0]

        tmp_file_path = str(tmp_path_factory.getbasetemp().joinpath(f"normalized.txt"))
        Measurement.countAverageAndSave([m1, m2], tmp_file_path)
        average = Measurement()
        average.loadFromFile(tmp_file_path)
        assert average.spectrumList == [1, 1, 1]
