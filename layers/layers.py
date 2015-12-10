__author__ = 'Sourabh'
import countlayer, frequencylayer, indexlayer, probabilitylayer
import numpy as np



class layer():

    data = []
    order = int
    type = str

    def __init__(self):
        pass

    def setdata(self, data):
        self.data = data

    def printdata(self, layer):
        layernp = np.asarray(layer.data)
        x, y = layernp.shape
        print x,y

    def setlayertype(self, type):
        if type == 'index':
            self.order = 0
            self.type = type
            return indexlayer.indexlayer(self.order, self.data)
        elif type == 'count':
            self.order = 1
            return countlayer.countlayer(self.order, self.data)
        elif type == 'freq':
            self.order = 2
            return frequencylayer.frequencylayer(self.order, self.data)
        elif type == 'prob':
            self.order = 3
            return probabilitylayer.probabilitylayer(self.order, self.data)
        else:
            print "No layer type specified"