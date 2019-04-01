import math
import os

#Length Conditioned n-gram Payload Model

class PaylModel(object):
    DIRNAME = "models"
    EXT_FILENAME = ".payl"

    def __init__(self, port, length):
        self.port = port
        self.length = length
        self.grams = {}
        # print self.grams
        # Creating a file for the payl model according to the length.
        self.filename = self.DIRNAME + "/" + str(self.port) + "-" + str(self.length) + self.EXT_FILENAME

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

    def save(self):
        if not os.path.isdir(self.DIRNAME): #assumes path exists
            os.mkdir(self.DIRNAME) #create a directory

        fmodel = open(self.filename, "w") #check write permision
        if not fmodel:
            print "failed to write (Did not save model)"
            return

        for key, value in self.grams.items():
            fmodel.write(str(key) + ";" + str(value.mean) + ";" + str(value.stddev) + ";" + str(value.count) + "\n")

        fmodel.close()
        print "Model " + str(self.port) + "-" + str(self.length) + " was sucsessfully saved!"

    def load(self):
        if not os.path.exists(self.filename):
            print "No file for model " + str(self.port) + "-" + str(self.length)
            return

        fmodel = open(self.filename, "r") #makes sure its readable

        for line in fmodel.readlines():
            splitted = line.split(";")
            # print splitted
            ByteFrequenci = ByteFrequency()
            ByteFrequenci.mean = splitted[1]
            ByteFrequenci.stddev = splitted[2]
            ByteFrequenci.count = splitted[3]
            self.grams[splitted[0]] = ByteFrequenci

        fmodel.close()

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
