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
        self.sonnet_train = self.tokenize(os.path.join(path, 'sonnets_train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'sonnets_dev.txt'))
        self.test = self.tokenize(os.path.join(path, 'sonnets_test.txt'))
        self.hymns = self.tokenize(os.path.join(path, 'hymns_no_urls.txt'))
        self.train = torch.cat((self.sonnet_train, self.hymns), 0)

    def tokenize(self, path):
        assert os.path.exists(path)
        # Add words to the dictionary
        longest_sentence = 0
        with open(path, 'r', encoding="utf8") as f:
            tokens = 0
            for line in f:
                line = line.split('\t')[0]
                words = line.split() + ['<eos>']
                if len(words) > 14 or len(words) < 7:
                    pass
                else:
                    while len(words) < 14:
                        words.append('<blank>')
                    words.append('<eol>')
                    if len(words) > longest_sentence:
                        longest_sentence = len(words)
                    tokens += len(words)
                    for word in words:
                        if not word in ['<eos>', '<blank>', '<eol>']:
                            word = re.sub(r'[^\w\s]', '', word)
                        self.dictionary.add_word(word)
            print(tokens)
            print("sentence max: " + str(longest_sentence))

        # Tokenize file content
        with open(path, 'r', encoding="utf8") as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                line = line.split('\t')[0]
                words = line.split() + ['<eos>']
                if len(words) > 14 or len(words) < 7:
                    pass
                else:
                    while len(words) < 14:
                        words.append('<blank>')
                    words.append('<eol>')
                    if len(words) > longest_sentence:
                        longest_sentence = len(words)
                    tokens += len(words)
                    for word in words:
                        if not word in ['<eos>', '<blank>', '<eol>']:
                            word = re.sub(r'[^\w\s]', '', word)
                        ids[token] = self.dictionary.word2idx[word]
                        token += 1
        return ids

