import readCMU

class HaikuTest(object):
    def __init__(self, CMUdict):
        self.CMUdict = CMUdict
        self.rhyme_words = {}
        self.syllable_count = 0
        self.line_number = 0
        self.syllables_per_line = [5, 7, 5]
        self.haiku_words = []

    def accepts(self, next_word):
        if self.line_number >= len(self.syllables_per_line):
            return False
        num_syllables = len(self.CMUdict.get_stresses(next_word))
        if num_syllables + self.syllable_count > self.syllables_per_line[self.line_number]:
            return False
        elif num_syllables + self.syllable_count < self.syllables_per_line[self.line_number]:
            self.syllable_count += num_syllables
            self.haiku_words.append(next_word)
        elif num_syllables + self.syllable_count == self.syllables_per_line[self.line_number]:
            self.rhyme_words[self.line_number] = next_word
            # TODO if the lines rhyme, continue
            self.line_number += 1
            self.syllable_count = 0
            self.haiku_words.append(next_word)
        return True

haiku = HaikuTest(readCMU.CMUDict("../data/cmudict.txt"))
print(haiku.accepts('hello')) # true
print(haiku.accepts('there')) # true
print(haiku.accepts('general')) # false
print(haiku.accepts('kenobi')) # false
print(haiku.accepts('you')) # true
print(haiku.accepts('are')) # true, new line
print(haiku.line_number)
print(haiku.accepts('a')) # true
print(haiku.accepts('bold')) # true
print(haiku.accepts('one')) # true
print(haiku.accepts('amazing')) # true
print(haiku.accepts('fantastic')) # false
print(haiku.accepts('superb')) # false
print(haiku.accepts('are')) # true, new line
print(haiku.line_number)
print(haiku.accepts('hello')) # true
print(haiku.accepts('there')) # true
print(haiku.accepts('general')) # false
print(haiku.accepts('kenobi')) # false
print(haiku.accepts('you')) # true
print(haiku.accepts('are')) # true, new line
print(haiku.line_number)
print(haiku.accepts('hello')) # false
print(haiku.accepts('there')) # false
print(haiku.line_number)