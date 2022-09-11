import os
import argparse
import numpy as np

punctuation = "!,-.:;?"
upperCase = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
lowerCase = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

class Model(object):
    def __init__(self):
        self.seq = [[],[],[]]
    def read(self, modelFile):
        with open(modelFile, 'r') as file:
            return eval(file.readline())
    def cleaning_tokenization(self, text):
        word = ""
        words = []
        for i in range(len(text)):
            if (text[i] in upperCase):
                pos = upperCase.find(text[i])
                word += lowerCase[pos]
            if (text[i] in lowerCase):
                word += text[i]
            if (len(word) != 0 and (text[i] not in upperCase + lowerCase)):
                words.append(word)
                word = ""
            if (text[i] in punctuation):
                words.append(text[i])
        return words
    def twothreefourgramming(self, words):
        for i in range(len(words) - 1):
            self.seq[0].append([words[i], words[i + 1]])
        for i in range(len(words) - 2):
            self.seq[1].append([words[i], words[i + 1], words[i + 2]])
        for i in range(len(words) - 3):
            self.seq[1].append([words[i], words[i + 1], words[i + 2], words[i + 3]])
        (self.seq[0]).sort(key = lambda x: x[0])
        (self.seq[1]).sort(key = lambda x: x[0]+x[1])
        (self.seq[2]).sort(key = lambda x: x[0]+x[1]+x[2])
    def fit(self, f):
        with open(f, 'r') as file:
            text = ""
            for line in file.readlines():
                text += line
            words = self.cleaning_tokenization(text)
            self.twothreefourgramming(words)
    def fitall(self, trainDir):
        tree = os.walk(trainDir)
        for f in list(tree)[0][2]:
            self.fit(trainDir + "\\" + f)
    def write(self, modelFile):
        with open(modelFile, 'w') as file:
            file.write('[')
            for i in range(3):
                file.write('[')
                for j in range(len(self.seq[i])):
                    file.write('[')
                    for k in range(len(self.seq[i][j])):
                        file.write('\'')
                        file.write(self.seq[i][j][k])
                        file.write('\'')
                        if (k != (len(self.seq[i][j]) - 1)):
                            file.write(',')
                    file.write(']')
                    if (j != (len(self.seq[i]) - 1)):
                        file.write(',')
                file.write(']')
                if (i != (len(self.seq) - 1)):
                        file.write(',')
            file.write(']')

if (__name__ == "__main__"):
    
    parser = argparse.ArgumentParser(description="Fit the model")
    parser.add_argument('trainD', type=str, help='File with the model')
    parser.add_argument('modelF', type=str, help='Directory with training files')
    args = parser.parse_args()
    
    tink = Model()
    tink.fitall(args.trainD)
    tink.write(args.modelF)
