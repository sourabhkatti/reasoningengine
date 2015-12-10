__author__ = 'Sourabh'

class wordstore():

    word = ""
    conditions = []
    index = []

    def __init__(self, word, conditions, index):
        self.word = word
        self.conditions = [conditions]
        self.index = index

    def getword(self):
        return self.word

    def getconditions(self):
        return self.conditions

    def getindex(self):
        return self.index