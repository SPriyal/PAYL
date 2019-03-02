import math
import os

#Length Conditioned n-gram Payload Model

class PaylModel(object):

    def __init__(self, port, length):
        self.port = port
        self.length = length
        self.grams = {}
        # print self.grams

    #creating a model considering which charecter occured how many times
    def add_grams(self, grams):
        # print grams
        for key, value in grams.items():
            self.add_gram(key, value)

    #Read gram as a charecter and gram_freq as the occurance of the charecter.
    def add_gram(self, gram, gram_freq):
        # print gram
        # print gram_freq
        if gram in self.grams:
            self.grams[gram].add_item(gram_freq)
        else:
            self.grams[gram] = ByteFrequency()
            self.grams[gram].add_item(gram_freq)

    def distance(self, new_model):
        dist = 0
        alpha = 0.001

        for i in range(0, 256):
            if str(i) in self.grams:
                # print str(i)
                old_mean = self.grams[str(i)].mean
                old_stddev = self.grams[str(i)].stddev
            elif i in self.grams:
                old_mean = self.grams[i].mean
                old_stddev = self.grams[i].stddev
            else:
                old_mean = 0
                old_stddev = 0

            if i in new_model:
                # print new_model
                new_gram = new_model[i]
            elif str(i) in new_model:
                # print new_model
                # print new_gram
                new_gram = new_model[str(i)]
                # print new_gram
            else:
                new_gram = 0


            substracted_mean = float(old_mean) - float(new_gram)
            if substracted_mean < 0:
                substracted_mean *= -1

            tmp = (substracted_mean / (float(old_stddev) + alpha))
            dist += tmp

        return dist

class ByteFrequency(object):
    def __init__(self):
        self.mean = 0
        self.stddev = 0
        self.count = 0

    def add_item(self, gram_freq):
        old_count = self.count
        self.count += 1
        old_mean = self.mean
        self.mean = ((self.mean * old_count) + gram_freq) / float(self.count)

        old_var = math.pow(self.stddev, 2)
        old_stdddev = self.stddev
        if self.count > 1:
            self.stddev = math.sqrt((((self.count - 2) / float(self.count - 1)) * old_var) + ((pow(gram_freq - old_mean, 2)) / float(self.count)))
        else:
            self.stddev = 0

    def __str__(self):
        return "Mean : " + str(self.mean) + "; Stddev : " + str(self.stddev) + "\n"
