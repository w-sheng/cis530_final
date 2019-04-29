class CMUDict(object):

    def __init__(self, cmu_dict_path):
        self.cmu_dict_path = cmu_dict_path
        self.pronunciations = {}
        self.stresses = {}
        self.create_CMU_dictionary()
        self.vowels = ['aa', 'ae', 'ah', 'ao', 'aw', 'ax', 'axr', 'ay', 'eh', 'er', 'ey', 'ih', 'ix', 'iy', 'ow', 'oy', 'uh', 'uw', 'ux']

    def create_CMU_dictionary(self):
        fin = open(self.cmu_dict_path, 'r', errors='ignore')
        raw_line = fin.readline()
        while raw_line[0] == ';':
            raw_line = fin.readline()
        while len(raw_line) > 0:
            split_line = raw_line.strip().split(' ')
            word = split_line[0]
            raw_syllables = split_line[2::]
            pronunciations = []
            stresses = []
            for raw_s in raw_syllables:
                if len(raw_s) > 0 and raw_s[-1].isdigit():
                    pronunciations.append(raw_s[:-1].lower())
                    stresses.append(int(raw_s[-1]))
                else:
                    pronunciations.append(raw_s.lower())
            self.pronunciations[word.lower()] = pronunciations
            self.stresses[word.lower()] = stresses
            raw_line = fin.readline()
        fin.close()

    # Returns the number of phonemes in the last syllable
    def num_phonemes_last_syllable(self, pronun):
        pronun = pronun[::-1]
        last = len(pronun)
        for vowel in self.vowels:
            if vowel in pronun and pronun.index(vowel) < last:
                last = pronun.index(vowel)
        return last + 1

    # Returns true if the two words rhyme, false otherwise
    # Returns false is one or both words are not in the dictionary
    def is_rhyme_words(self, word1, word2):
        if word1 in self.pronunciations and word2 in self.pronunciations:
            pronun1 = self.pronunciations[word1]
            pronun2 = self.pronunciations[word2]
            word1_num_phonemes = self.num_phonemes_last_syllable(pronun1)
            word1_last_syllable = pronun1[-1 * word1_num_phonemes:]
            word2_num_phonemes = self.num_phonemes_last_syllable(pronun2)
            word2_last_syllable = pronun2[-1 * word2_num_phonemes:]
            if word1_last_syllable == word2_last_syllable:
                return True
        return False
    
    # Returns a list representing the IPA pronunciation of the given word
    # Returns an empty list if word is not in dictionary
    def get_pronunciation(self, word):
        return self.pronunciations[word] if word in self.pronunciations else []

    # Returns a list representing the stressed and unstressed syllables of the given word, where 0 = unstressed and 1 = stressed
    # Returns an empty list if word is not in dictionary
    def get_stresses(self, word):
        return self.stresses[word] if word in self.pronunciations else [0 if (i % 2 == 0) else 1 for i in range(int(len(word)/3))]

cmudict = CMUDict("../data/cmudict.txt")
# print(cmudict.get_pronunciation('abate'))
# print(cmudict.get_stresses('abate'))
# print(cmudict.get_pronunciation('bore'))
# print(cmudict.get_stresses('bore'))
# print(cmudict.get_pronunciation('knight'))
# print(cmudict.get_stresses('knight'))
# print(cmudict.get_pronunciation('zebra'))
# print(cmudict.get_stresses('zebra'))
# print(cmudict.is_rhyme_words('flight', 'knight'))
# print(cmudict.is_rhyme_words('shooting', 'dying'))
# print(cmudict.is_rhyme_words('debate', 'cremate'))

