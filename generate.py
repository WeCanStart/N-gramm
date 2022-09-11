import os
import argparse
import numpy as np

punctuation = "!,-.:;?"
upperCase = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
lowerCase = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def binary_search_two(data, elem):
    low = 0
    high = len(data) - 1
    while low <= high:
        middle = (low + high)//2
        if data[middle][0] == elem:
            l, r = middle, middle
            while (data[l][0]) == elem:
                l-=1
            while (data[r][0]) == elem:
                r+=1
            return l, r
        elif data[middle][0] > elem:
            high = middle - 1
        else:
            low = middle + 1
    return [-1, -1]
def binary_search_three(data, elem):
    low = 0
    high = len(data) - 1
    while low <= high:
        middle = (low + high)//2
        if (data[middle][0] + data[middle][1]) == elem:
            l, r = middle, middle
            while (data[l][0] + data[l][1]) == elem:
                l-=1
            while (data[r][0] + data[r][1]) == elem:
                r+=1
            return l, r
        elif (data[middle][0] + data[middle][1]) > elem:
            high = middle - 1
        else:
            low = middle + 1
    return [-1, -1]
def binary_search_four(data, elem):
    low = 0
    high = len(data) - 1
    while low <= high:
        middle = (low + high)//2
        if (data[middle][0] + data[middle][1] + data[middle][2]) == elem:
            l, r = middle, middle
            while (data[l][0] + data[l][1] + data[l][2]) == elem:
                l-=1
            while (data[r][0] + data[r][1] + data[r][2]) == elem:
                r+=1
            return l, r
        elif (data[middle][0] + data[middle][1] + data[middle][2]) > elem:
            high = middle - 1
        else:
            low = middle + 1
    return [-1, -1]

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
        (self.seq[1]).sort(key = lambda x: x[0]+x[1]+x[2])
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

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description="Generate sequence")
    parser.add_argument('modelF', type=str, help='File with the model')
    parser.add_argument('prefix', type=str, help='Some first words', nargs = '+')
    parser.add_argument('length', type=int, help='How many words do we have to add')
    args = parser.parse_args()
    
    tink = Model()
    start = args.prefix
    gramms = tink.read(args.modelF)
    
    i = 0
    if len(start)==1:
        pos = binary_search_two(gramms[0], start[0])
        if pos == [-1, -1]:
            print("Несоответствие базе")
            exit()
        else:
            i+=1
            start.append(gramms[0][np.random.randint(pos[0] + 1, pos[1])][1])
    if len(start)==2:
        pos = binary_search_three(gramms[1], start[i-1]+start[1])
        if pos == [-1, -1]:
            pos = binary_search_two(gramms[0], start[i-1])
            if pos == [-1, -1]:
                print("Несоответствие базе")
                exit()
            else:
                i+=1
                start.append(gramms[0][np.random.randint(pos[0] + 1, pos[1])][1])
        else:
            i+=1
            start.append(gramms[1][np.random.randint(pos[0] + 1, pos[1])][2])
            
    while (i < args.length):
        pos = binary_search_four(gramms[2], start[i-3]+start[i-2]+start[i-1])
        if pos == [-1, -1]:
            pos = binary_search_three(gramms[1], start[i-2]+start[i-1])
            if pos == [-1, -1]:
                pos = binary_search_two(gramms[0], start[i-1])
                if pos == [-1, -1]:
                    print("Несоответствие базе")
                    exit()
                else:
                    i+=1
                    start.append(gramms[0][np.random.randint(pos[0] + 1, pos[1])][1])
            else:
                i+=1
                start.append(gramms[1][np.random.randint(pos[0] + 1, pos[1])][2])
        else:
            i+=1
            start.append(gramms[2][np.random.randint(pos[0] + 1, pos[1])][3])
    print(start)
