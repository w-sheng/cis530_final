import readCMU
from nltk.tokenize import word_tokenize

class SonnetFSA(object):
    def __init__(self, CMUdict):
        self.CMUdict = CMUdict
        self.rhyme_words = {}
        self.syllable_count = 0
        self.line_number = 0
        self.syllables_per_line = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        self.rhyme_scheme = {2:{0},3:{1},6:{4},7:{5},10:{8},11:{9},13:{12}} # dictionary mapping line to set of previous lines that must rhyme with it
        self.sonnet_words = []

    # Given a lower case word, returns true if the word fits in terms of syllable count and rhyme scheme
    def accepts(self, next_word):
        if self.line_number >= len(self.syllables_per_line):
            return 3
        num_syllables = len(self.CMUdict.get_stresses(next_word))
        if num_syllables == 0:
            return 1
        else:
            if num_syllables + self.syllable_count > self.syllables_per_line[self.line_number]:
                return 1
            elif num_syllables + self.syllable_count < self.syllables_per_line[self.line_number]:
                if self.syllable_count == 0:
                    # handle rhyme
                    if self.line_number in self.rhyme_scheme:
                        for line_num in self.rhyme_scheme[self.line_number]:
                            if not self.CMUdict.is_rhyme_words(next_word, self.rhyme_words[line_num]):
                                return 1
                    self.rhyme_words[self.line_number] = next_word
                self.syllable_count += num_syllables
                self.sonnet_words.append(next_word)
                return 0
            elif num_syllables + self.syllable_count == self.syllables_per_line[self.line_number]:
                self.line_number += 1
                self.syllable_count = 0
                self.sonnet_words.append(next_word)
                return 2
        # return True

    # Resets to starting state of the FSA - use this method if you're feeding in a new sonnet
    def reset(self):
        self.rhyme_words = {}
        self.syllable_count = 0
        self.line_number = 0
        self.sonnet_words = []

    def getWordToRhymeWith(self):
        if self.line_number in self.rhyme_scheme:
            prev_lines = self.rhyme_scheme[self.line_number]
            for line_num in prev_lines:
                if line_num in self.rhyme_words:
                    return self.rhyme_words[line_num]
        return ''

# Example usage
# sonnetFSA = SonnetFSA(readCMU.CMUDict("data/cmudict.txt"))
# fin = open('data/easy_sonnet.txt', 'r', errors='ignore')
# line = fin.readline()
# while len(line) > 0:
#     words = [word.lower() for word in word_tokenize(line) if word.isalpha()]
#     for word in words:
#         print(word, sonnetFSA.syllable_count, sonnetFSA.line_number, sonnetFSA.accepts(word))
#     line = fin.readline()