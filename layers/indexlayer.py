__author__ = 'SourabhKatti'
import layers


class indexlayer():

    order = 0
    indices = []
    data = []

    def __init__(self, order, data):
        print "Success index layer object!!"
        self.order = order
        self.data = data
        self.indices = self.data

    def setorder(self, order):
        self.order = order

    def getdata(self):
        return self.indices

