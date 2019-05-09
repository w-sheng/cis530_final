

def odds_ratio(path_1, path_2):
    with open(path_1, 'r', encoding='utf-8', errors='ignore') as file:
        word_frequency_1 = {}
        total_words_1 = 0
        for line in file:
            words = line.split()
            for word in words:
                total_words_1 += 1
                if word in word_frequency_1:
                    word_frequency_1[word] += 1
                else:
                    word_frequency_1[word] = 0
    for word in word_frequency_1:
        word_frequency_1[word] /= total_words_1

    with open(path_2, 'r', encoding='utf-8', errors='ignore') as file:
        word_frequency_2 = {}
        total_words_2 = 0
        for line in file:
            words = line.split()
            for word in words:
                total_words_2 += 1
                if word in word_frequency_2:
                    word_frequency_2[word] += 1
                else:
                    word_frequency_2[word] = 0
    for word in word_frequency_2:
        word_frequency_2[word] /= total_words_2

    odds_ratios = {}
    for word in word_frequency_1:
        try:
            p1 = word_frequency_1[word]
            p2 = word_frequency_2[word]
            q1 = 1 - p1
            q2 = 1 - p2
            odds_ratios[word] = p1 * q2 / (p2 * q1)
        except:
            odds_ratios[word] = float('inf')
    for word in word_frequency_2:
        if word not in odds_ratios:
            odds_ratios[word] = 0

    return odds_ratios

if __name__ == "__main__":
    OR = odds_ratio('trash1.txt', 'trash2.txt')
    for word in OR:
        if OR[word] != float('inf') and OR[word] != 0:
            print('%s: %.3f' % (word, OR[word]))
