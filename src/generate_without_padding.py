from odds_ratio import odds_ratio
from random import shuffle
import requests
import argparse
import torch
import utility
import readCMU
import FSA_quatrain_rev as fsa # CHANGE TO FSA OF CHOSEN POEM CATEGORY


parser = argparse.ArgumentParser(description='PyTorch sonnets Language Model')

# Model parameters.
parser.add_argument('--data', type=str, default='../data',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='../src/models/model_v4_rev.pt',
                    help='model checkpoint to use')
parser.add_argument('--outf', type=str, default='generated.txt',
                    help='output file for generated text')
parser.add_argument('--words', type=int, default='500',
                    help='number of words to generate')
parser.add_argument('--seed', type=int, default=44,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
parser.add_argument('--log-interval', type=int, default=20,
                    help='reporting interval')
args = parser.parse_args()

# Set the random seed manually for reproducibility.
torch.manual_seed(args.seed)
if torch.cuda.is_available():
    if not args.cuda:
        print("WARNING: You have a CUDA device, so you should probably run with --cuda")

device = torch.device("cuda" if args.cuda else "cpu")

if args.temperature < 1e-3:
    parser.error("--temperature has to be greater or equal 1e-3")

with open(args.checkpoint, 'rb') as f:
    model = torch.load(f, map_location='cpu').to(device)
model.eval()

# set up corpus
corpus = utility.Corpus(args.data, "nopadding")

# create histories for input layers
input_histories = utility.input_dict(5)

# set the first input tensor to be <eol>
ntokens = len(corpus.dictionary)
hidden = model.init_hidden(1)
input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
print("starting with the token <eos>: ")
print(corpus.dictionary.word2idx['<eos>'])
input.fill_(corpus.dictionary.word2idx['<eos>'])
input_histories.add(input.data.clone())

# create FSA
sonnetFSA = fsa.QuatrainFSA(readCMU.CMUDict("../data/cmudict.txt")) # CHANGE THE FSA TO THE POEM CATEGORY

# some other inits
blank_flag = False
end_flag = False

URL = 'https://api.datamuse.com/words'

# Randomly shuffle the words with the top 4000 odds ratio
odds_data = odds_ratio('../data/hymns/hymns_no_urls_rev.txt', '../data/nytimes_news_articles.txt')
randomized_odds = [tup[0] for tup in sorted(odds_data.items(), key=lambda kv: kv[1])][-4000:]
shuffle(randomized_odds)
line_number = 1

with open('generated_nopadding.txt', 'w') as outf:
    with open('options.txt', 'w') as tmpf:
        with torch.no_grad():
            new_line = True
            for i in range(args.words):
                print("\n\n\n")
                print("at the " + str(i) + "th iteration.")
                output, hidden = model(input, hidden)
                word_weights = output.squeeze().div(args.temperature).exp().cpu()
                words_idx = torch.multinomial(word_weights, 100)

                # record some of the top options
                words_tmp = []
                for j in range(0, 10):
                    words_tmp.append(corpus.dictionary.idx2word[words_idx[j]])
                tmpf.write(str(words_tmp) + '\n')

                # record the first word
                words_idx_list = words_idx.tolist()
                first = words_idx_list[0]

                # generation loop with FSA
                for k in range(0, len(words_idx_list)):
                    # if there's a new line, handle the rhyme scheme properly (everything is reversed so the first word of the line must rhyme)
                    if new_line:
                        word_to_rhyme_with = sonnetFSA.getWordToRhymeWith()
                        if len(word_to_rhyme_with) > 0: # have to find something that rhymes with word_to_rhyme_with
                            r = requests.get(url = URL, params = {'rel_rhy' : word_to_rhyme_with}).json()
                            if len(r) > 0:
                                odds = [odds_data[response['word']] if response['word'] in odds_data and response['word'] in corpus.dictionary.idx2word else 0 for response in r]
                                fsa_word = r[odds.index(max(odds))]['word']
                                word = fsa_word
                        else: # otherwise, find a word that exists in the corpus and rhymes with words that also exist in the corpus
                            high_odds = corpus.dictionary.idx2word[words_idx_list[k]]
                            for i in range(len(randomized_odds) // line_number):
                                high_odds = randomized_odds[(i + 1) * line_number]
                                r = requests.get(url = URL, params = {'rel_rhy' : high_odds}).json()
                                contains_word_in_corpus = False
                                for response in r:
                                    if response['word'] in corpus.dictionary.idx2word:
                                        contains_word_in_corpus = True
                                if contains_word_in_corpus:
                                    break
                            word = high_odds
                            fsa_word = high_odds.lower()
                        new_line = False
                    else:
                        word = corpus.dictionary.idx2word[words_idx_list[k]]
                        fsa_word = corpus.dictionary.idx2word[words_idx_list[k]].lower()
                    if word == '<eos>':
                        # print("RNN think it should end but FSA want to keep going")
                        input.fill_(corpus.dictionary.word2idx[word])
                        input_histories.add(input.data.clone())
                    else:
                        print(fsa_word)
                        FSA_decision = sonnetFSA.accepts(fsa_word)
                        # case the word accepted
                        if FSA_decision == 0:
                            print("accepted: " + word)
                            outf.write(word + ' ')
                            input.fill_(corpus.dictionary.word2idx[word])
                            input_histories.add(input.data.clone())
                            new_line = False
                            break
                        # case the word not accepted
                        elif FSA_decision == 1:
                            print("declined: " + word)
                            pass
                        # case the word accepted and wo need to break into next line
                        elif FSA_decision == 2:
                            print("accepted: " + word + " and next line")
                            outf.write(word + '\n')
                            line_number += 1
                            input.fill_(corpus.dictionary.word2idx[word])
                            input_histories.add(input.data.clone())
                            new_line = True
                            break
                        # reached max length of a sonnet
                        elif FSA_decision == 3:
                            end_flag = True
                            break
                if end_flag:
                    break
print('DONE')
