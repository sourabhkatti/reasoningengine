__author__ = 'Sourabh'

import wordstore

class linestore():

    wordsinline = []
    conditions = []

    def __init__(self, words):
        for word in words:
            self.wordsinline.append(word)
            self.conditions.append(word)

