from nltk.tokenize import word_tokenize
import string

# REVERSE TRAINING DATA

# with open('../data/poem_generation_data/sonnets_train.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/poem_generation_data/sonnets_train_rev.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             fout.write(" ".join(word_tokenize(line[:-2])[::-1]) + '\n')
#             line = fin.readline()
# with open('../data/hymns/hymns_no_urls.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/hymns/hymns_no_urls_rev.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             fout.write(" ".join(word_tokenize(line)[::-1]) + '\n')
#             line = fin.readline()
# with open('../data/lyrics.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/lyrics_rev_v2.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             raw_line = [word for word in word_tokenize(line)[::-1] if len(word) < 15]
#             fout.write(" ".join(raw_line) + '\n')
#             line = fin.readline()

# REVERSE GENERATED POEM

with open('generated_nopadding.txt', 'r', encoding='utf-8', errors='ignore') as fin:
    with open('generated_corrected.txt', 'w', encoding='utf-8', errors='ignore') as fout:
        line = fin.readline()
        while len(line) > 0:
            fout.write(" ".join(word_tokenize(line)[::-1]) + '\n')
            line = fin.readline()

# REMOVE MALFORMED CHARACTERS FROM DATASETS

# def isWordWithPunc(word):
#     for char in word:
#         if not char.isalpha() and char != '…' and char != '—' and char != '´' and char != '´' and char != '“' and char != '’' and char != '‘':
#             return False
#     return True
#
# with open('../data/poem_generation_data/sonnets_train.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/poem_generation_data/sonnets_train_rev.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             modified_line = [word.translate(str.maketrans('', '', string.punctuation)) for word in word_tokenize(line)]
#             removeLine = False
#             for word in modified_line:
#                 if not isWordWithPunc(word) and len(word) > 0 and not word.isdigit():
#                     removeLine = True
#                     break
#             if not removeLine:
#                 fout.write(line)
#             line = fin.readline()
# with open('../data/hymns/hymns_no_urls.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/hymns/hymns_no_urls_rev.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             modified_line = [word.translate(str.maketrans('', '', string.punctuation)) for word in word_tokenize(line)]
#             removeLine = False
#             for word in modified_line:
#                 if not isWordWithPunc(word) and len(word) > 0 and not word.isdigit():
#                     removeLine = True
#                     break
#             if not removeLine:
#                 fout.write(line)
#             line = fin.readline()
# with open('../data/lyrics.txt', 'r', encoding='utf-8', errors='ignore') as fin:
#     with open('../data/lyrics_rev.txt', 'w', encoding='utf-8', errors='ignore') as fout:
#         line = fin.readline()
#         while len(line) > 0:
#             modified_line = [word.translate(str.maketrans('', '', string.punctuation)) for word in word_tokenize(line)]
#             removeLine = False
#             for word in modified_line:
#                 if not isWordWithPunc(word) and len(word) > 0 and not word.isdigit():
#                     removeLine = True
#                     break
#             if not removeLine:
#                 fout.write(line)
#             line = fin.readline()