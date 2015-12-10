__author__ = 'Sourabh'
from collections import defaultdict
import os
import re
import time

from gensim import models,corpora

import layers.layers as layer
from lineprocessingutils import *


class reasoningengine():
    re_name = 'reasoningengine'
    re_version = 'v1.0'

    logs = {}           # Log file number => log file name
    sentences = {}      # Sentence number => list of words in the sentence
    words = {}          # Word number => word

    log_to_sentence = {}    # Holds the index mapping between each log and its sentences
    sentence_to_word = {}   # Holds the index mapping between each sentence and its words

    word_properties = {}


    layers = {}
    layermanager = layer.layer()


    current_line = []
    current_log = []
    use_stored_terms = False





    def __init__(self, use_stored_terms,logstoadd=2):
        print self.re_name + " " + self.re_version  + "\n\n"
        self.use_stored_terms = use_stored_terms
        self.init_engine(logstoadd)


    def init_engine(self, logstoadd):
        if self.use_stored_terms:
            self.init_linemodel(use_vocab_file=True)
            self.generate_sentences_corpora(use_corpus_file=True)
        else:
            self.addsentences(logstoadd)
            self.init_linemodel()
            self.generate_sentences_corpora()

    # Get the raw list of words from which we'll setup the dictionary
    def addsentences(self, traininglogs_root='C:/logpredict/logpredict/li_train', logstoadd = 25):
        traininglogs_root='C:/reasoningengine/testlogs'
        print "Parsing training logs at", traininglogs_root
        logs_count = 0
        for raw_log in os.listdir(traininglogs_root):
            t1 = time.time()
            print "\tAdding",
            print ('{:.<50}'.format(raw_log)),
            count_ls = []

            filename = traininglogs_root+'/'+raw_log
            sentence_count = 0

            # Read all lines in the log. Update internal dictionary with the sentences.
            with open(filename, 'r') as f:
                raw_sentences = f.readlines()
            for sentence in raw_sentences:
                sentencefinal = []
                split_sentence=sentence.split(" ")
                for term in split_sentence:
                    if re.match("[\'a-zA-Z\[]+",term):
                        sentencefinal.append(term)
                count_ls.append(sentence_count)
                index = self.sentences.__len__()
                self.sentences[index]=sentencefinal
                sentence_count+=1
            self.logs[logs_count]=raw_log
            self.log_to_sentence[logs_count]=count_ls
            t2 = time.time()
            print 'Success',
            print t2-t1
            logs_count+=1
            if logs_count == logstoadd:
                break

    # Setup Word2Vec model for every word on each sentence
    def init_linemodel(self, use_vocab_file=False):

        if not use_vocab_file:
            # Build a dictionary of the words
            frequency = defaultdict(int)
            linevocabulary = corpora.Dictionary(list(self.sentences.values()))
            linevocabulary.save('sentences_vocabulary.dict')

            # Build word-to-vector model out of the logs
            linemodel = models.Word2Vec(list(self.sentences.values()), size=100, window=3, workers=4)
            linemodel.save('linemodel.vocabulary')

        self.linevocabulary = corpora.Dictionary.load('sentences_vocabulary.dict')
        self.linemodel = models.Word2Vec.load('linemodel.vocabulary')

        print ("Model created from sentences, vocabulary contains %d words." % self.linemodel.vocab.__len__())
        #pprint(linemodel.vocab)

        self.init_wordmodel(use_vocab_file)

    # Setup Word2Vec model for each term in a word
    def init_wordmodel(self, use_vocab_file=False):
        t1 = time.time()
        logwords = {}
        if not use_vocab_file:
            linesize = self.linemodel.vocab.__len__()

            for i in range(0, self.linevocabulary.__len__()):
                raw_word= self.linevocabulary.get(i)
                # Split the word on any special characters
                #words = raw_word.split(r"([\=\_\.\-\[\]\(\)\\:\;\'\/\?\>\<\\\]+)")
                words = re.split(r"[\.\=\n\(\)\:\]\\n\$\/\\\\]+", raw_word)
                #words = raw_word.split('')
                CHARACTER_COUNT = raw_word.__len__()

                if words.__len__() > 1:
                    CAN_BE_SPLIT = 1

                    logwords[i]=words
                    for word in words:
                        if re.match("[\'a-zA-Z\[]+",word):
                            if word not in list(self.words.keys()):
                                self.words[word]=[self.linevocabulary.token2id[raw_word]]
                            else:
                                token = self.linevocabulary.token2id[raw_word]
                                tokens = self.words[word]
                                tokens.append(token)
                                tokens = list(set(tokens))
                                self.words[word]=tokens
                else:
                    CAN_BE_SPLIT=0
                properties = [CAN_BE_SPLIT, CHARACTER_COUNT]
                self.word_properties[raw_word]=properties


            wordmodel = models.Word2Vec(list(logwords.values()), size = 100, window=5, workers=4)
            wordmodel.save('wordmodel.vocabulary')

            wordvocabulary = corpora.Dictionary(list(logwords.values()))
            wordvocabulary.save('word_vocabulary.dict')

        self.wordvocabulary = corpora.Dictionary.load('word_vocabulary.dict')
        self.wordmodel = models.Word2Vec.load('wordmodel.vocabulary')
        t2 = time.time()
        print ("Model created from words in sentences, vocabulary contains %d words." % self.wordmodel.vocab.__len__())
        print "\tTotal time to run: ",t2-t1
        #pprint(wordmodel.vocab)

    def generate_sentences_corpora(self, use_corpus_file=True):
        t1 = time.time()
        if use_corpus_file:
            sentence_corpus = [self.linevocabulary.doc2bow(text) for text in list(self.sentences.values())]
            corpora.MmCorpus.serialize('sentence_corpus.mm', sentence_corpus)
        self.sentence_corpus = corpora.MmCorpus('sentence_corpus.mm')
        t2 = time.time()
        print("Corpora created of %d lines from log files" % self.sentence_corpus.num_docs)
        print "\tTotal time to run: ",t2-t1

    def sentencesimilarity(self, sentence):
        pass

    def generate_sentences_tfidf(self):
        self.sentences_tf = models.TfidfModel(self.sentence_corpus)

    def wordsimilarity(self, word):
        properties = []
        t1 = time.time()
        try:
            lista = (self.linemodel.most_similar(word, topn=5))

            print "\nThe following words are most similar to: %s" % word
            for term in lista:
                print "\t%s. '%s' with a probability of %f" % (self.linevocabulary.token2id[term[0]], term[0], term[1])
        except:
            try:
                words_2 = word.split(" ")
                for word in words_2:
                    lista = (self.linemodel.most_similar(word, topn=5))

                    print "\nThe following words are most similar to: %s" % word
                    for term in lista:
                        print "\t%s. '%s' with a probability of %f" % (self.linevocabulary.token2id[term[0]], term[0], term[1])
            except:
                print "\nThe word %s is not in the dictionary. Trying to parse it in other ways..." % word,



        t2 = time.time()
        print  t2-t1
        split_words = re.compile("([\=\_\.\-\[\]\(\)\\:\;\'\/\?\>\<\\\])").split(word)
        if split_words.__len__() > 1:
            t1 = time.time()
            for word in split_words:
                if re.match("[A-Za-z]+",word):
                    try:
                        print "\tAfter breaking down the word, the following words are most similar to: %s" % word
                        relatedwords = self.wordmodel.most_similar(word, topn=5)
                        for term in relatedwords:
                            print "\t\t%s. '%s' with a probability of %f" % (self.wordvocabulary.token2id[term[0]], term[0], term[1])
                    except:
                        print "The word %s doesn't have any similar words in the vocabulary" % word
            t2 = time.time()
            print "Total time to retrieve words: ", t2-t1


        else:
            print "Unable to break down the word %s from other words in the dictionary" % word

    def init_layers(self):
        self.gettrainingwords()
        self.layermanager.setdata(self.current_log)
        indexlayer = self.addlayer('index')
        countlayer = self.addlayer('count')
        freqlayer = self.addlayer('freq')
        problayer = self.addlayer('prob')

    def addlayer(self, type):
        layer = self.layermanager.setlayertype(type)
        self.layers[layer.order]=layer
        return layer

    def gettrainingwords(self):
        train_path = 'C:/reasoningengine/testlogs'
        for fileop in os.listdir(train_path):
            filetoopen = train_path+'/'+fileop
            with open(filetoopen, 'r') as f:
                self.current_log = f.readlines()
            for line in self.current_log:
                self.current_line = [line]

    def trainlayers(self):
        words = []
        for layer in self.layers.values():
            data = layer.getdata()
            x, y = decompose.getshape(data)
            decomposedwords, rules = decompose.decompose(data)








ree = reasoningengine(True)

#ree.wordsimilarity('WARNING: Error running progress')

ree.init_layers()
ree.trainlayers()

