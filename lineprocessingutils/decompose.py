__author__ = 'SourabhKatti'
import re
import linestore, wordstore
import numpy as np

class decomposer():

    conditions = {}
    rules = []


    def __init__(self):
        pass

    def decompose(self, log):
        logwords = []
        logrules = []
        for line in log:
            words, conditions = self.decomposeline(line)
            logwords.append(words)
            logrules.append(conditions)
        wl = self.generateobjects()
        return logwords, logrules

    def decomposeline(self, line):

        # Split the line by space
        spaces_words = self.spaces(line)
        if spaces_words == line:
            self.conditions['spaces']=[0]
        else:
            self.conditions['spaces']=[spaces_words]


        # Split each word in each line on every special character
        sc_words = self.specialcharacters(spaces_words)
        self.conditions['sc']=sc_words

        # Check every character in each line for specified conditions
        ct_words = self.checktypes(sc_words)
        self.conditions['ct']=ct_words





        return list(self.conditions.values()), spaces_words.__len__()

    def generateobjects(self):
        lines = []
        words = []
        spaces = self.conditions['spaces']
        spechars = self.conditions['sc']
        checktypes = self.conditions['ct']


        for i, line in enumerate(spechars):
            for j, word in enumerate(line):
                ct = []
                for k, letter in enumerate(word):
                    ct.append(checktypes[i][j][k])
                ws = wordstore.wordstore(word,ct,[i,j])
                words.append(ws)
            ls = linestore.linestore(words)
        return ls






    def spaces(self, line):
        words = re.split(" ",line)
        words = np.asarray(words)

        if words[0].__len__() > line[0].__len__():
            return words
        else:
            if words[1].__len__() > line[0].__len__():
                return words
            else:
                return line

    def checktypes(self, words):

        # Check the word if it's a number or contains capitals.
        # Returns an array [[[[conditions]/letter]/word]/sentence]/logs
        #     where [conditions] = an array of 1s and 0s of each condition above

        cap_log = []
        for line in words:
            print line
            cap_line = []
            for word in line:
                cap_word = []
                for letter in word:
                    cap_letter = []
                    if letter.isupper()==True:
                        cap_letter.append(1)
                    else:
                        cap_letter.append(0)

                    if letter.isdigit()==True:
                        cap_letter.append(1)
                    else:
                        cap_letter.append(0)

                    if letter == '\t':
                        cap_letter.append(1)
                    else:
                        cap_letter.append(0)

                    cap_word.append(cap_letter)
                cap_line.append(cap_word)
            cap_log.append(cap_line)
        return cap_log

    def specialcharacters(self, words):

        # Check for any special characters in the word and remove them if they are.

        sc = '\s'
        rsc = re.compile(sc)
        wordstoreturn = []
        size = words[0].__len__()
        wordsc = []

        if size > 1:
            for word in words:
                wordsplit = re.split('[\-\:\[\]\.\(\)\=\_\;\'\,\/\\\\\\n]+',word)
                for wordp in wordsplit:
                    if not (wordp == '' or wordp == "''"):
                        wordsc.append(wordp)
            wordstoreturn.append(wordsc)
        else:
            wordsc = re.split('[\-\:\[\]\.\(\)\=\_\;\'\,\/\\\\\\n]+',words)
            wordstoreturn.append([wordsc])

        return wordstoreturn



    def getshape(self, data):
        x = data.__len__()
        try:
            return x,0
        except:
            print 'error'




