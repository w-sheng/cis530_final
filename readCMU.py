class CMUDict(object):

    def __init__(self, cmu_dict_path):
        self.cmu_dict_path = cmu_dict_path
        self.pronunciations = {}
        self.stresses = {}
        self.create_CMU_dictionary()

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
    
    # Returns a list representing the IPA pronunciation of the given word
    # Returns an empty list if word is not in dictionary
    def get_pronunciation(self, word):
        return self.pronunciations[word] if word in self.pronunciations else []

    # Returns a list representing the stressed and unstressed syllables of the given word, where 0 = unstressed and 1 = stressed
    # Returns an empty list if word is not in dictionary
    def get_stresses(self, word):
        return self.stresses[word] if word in self.pronunciations else []

cmudict = CMUDict('data/cmudict.txt')
# print(cmudict.get_pronunciation('abate'))
# print(cmudict.get_stresses('abate'))
# print(cmudict.get_pronunciation('bore'))
# print(cmudict.get_stresses('bore'))
# print(cmudict.get_pronunciation('knight'))
# print(cmudict.get_stresses('knight'))
# print(cmudict.get_pronunciation('zebra'))
# print(cmudict.get_stresses('zebra'))