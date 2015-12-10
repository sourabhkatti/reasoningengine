__author__ = 'SourabhKatti'

import layers

class countlayer():

    order = 0
    data = []
    counts = []

    def __init__(self, order, data):
        print "Success countlayer object!!"
        self.order = order
        self.data = data



    def printword(self):
        print "Lets see if this works"

    def setorder(self, order):
        self.order = order

    def getdata(self):
        return self.counts