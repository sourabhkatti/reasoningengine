__author__ = 'SourabhKatti'

import layers

class frequencylayer():

    order = 0
    data = []
    frequencies = []

    def __init__(self, order, data):
        print "Success frequency layer object!!"
        self.order = order
        self.data = data

    def printword(self):
        print "Lets see if this works"

    def setorder(self, order):
        self.order = order

    def getdata(self):
        return self.frequencies
