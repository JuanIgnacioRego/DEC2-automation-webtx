from Data import sites
import QAPI, os

class LayerSwatch(object):

    @classmethod
    def setUp(cls):
        QAPI.unsetURLDinamica(sites["Swatch"], os.getenv("PPBLINK"), "C")


    @classmethod
    def tearDown(cls):
        QAPI.setURLDinamica(sites["Swatch"], "B") #restores to default config

    @classmethod
    def testSetUp (cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass

