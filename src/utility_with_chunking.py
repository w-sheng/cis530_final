import os
from io import open
import torch
import re


##############################################################################################
# parser
##############################################################################################


class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train/sonnets_train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'dev/sonnets_dev.txt'))
        self.test = self.tokenize(os.path.join(path, 'test/sonnets_test.txt'))

    def tokenize(self, path):
        assert os.path.exists(path)
        # Add words to the dictionary
        longest_sentence = 0
        with open(path, 'r', encoding="utf8") as f:
            tokens = 0
            for line in f:
                if len(line) > 3:
                    line = line.split('\t')[0]
                    words = line.split() + ['<eos>']
                    while len(words) < 12:
                        words.append('<blank>')
                    words.append('<eol>')
                    if len(words) > longest_sentence:
                        longest_sentence = len(words)
                    tokens += len(words)
                    for word in words:
                        word = word.lower()
                        if not word in ['<eos>', '<blank>', '<eol>']:
                            word = re.sub(r'[^\w\s]', '', word)
                        self.dictionary.add_word(word)
            print(path)
            print(tokens)
            print("longest sentence: " + str(longest_sentence))

        # Tokenize file content
        with open(path, 'r', encoding="utf8") as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                if len(line) > 3:
                    line = line.split('\t')[0]
                    words = line.split() + ['<eos>']
                    while len(words) < 12:
                        words.append('<blank>')
                    words.append('<eol>')
                    tokens += len(words)
                    for word in words:
                        word = word.lower()
                        if not word in ['<eos>', '<blank>', '<eol>']:
                            word = re.sub(r'[^\w\s]', '', word)
                        ids[token] = self.dictionary.word2idx[word]
                        token += 1
            return ids

# just realized this is a fucking stack
class input_dict(object):
    def __init__(self, max):
        self.dict = []
        self.length = 0
        self.max = max

    def __len__(self):
        return self.length

    def add(self, tensor):
        if self.length == self.max:
            self.dict = self.dict[1:]
            self.length -= 1
        self.dict.append(tensor)
        self.length += 1

    def pop(self):
        tmp = self.dict[0]
        self.dict = self.dict[1:]
        self.length -= 1
        return tmp

    def print(self):
        for entry in self.dict:
            print(entry)

