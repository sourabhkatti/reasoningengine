__author__ = 'SourabhKatti'

import layers

class probabilitylayer():

    order = 0
    data = []
    probabilities = []

    def __init__(self, order, data):
        print "Success probability layer object!!"
        self.order = order
        self.data = data

    def printword(self):
        print "Lets see if this works"

    def setorder(self, order):
        self.order = order

    def getdata(self):
        return self.probabilities