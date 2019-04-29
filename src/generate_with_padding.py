

import argparse
import torch
import utility
import readCMU
import FSA_sonnet_for_RNN as fsa

parser = argparse.ArgumentParser(description='PyTorch sonnets Language Model')

# Model parameters.
parser.add_argument('--data', type=str, default='../data',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='../src/models/model_ep80_nopad_comma.pt',
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
    model = torch.load(f).to(device)
model.eval()

# set up corpus
corpus = utility.Corpus(args.data, "padding")

# create histories for input layers
input_histories = utility.input_dict(5)

# set the first input tensor to be <eol>
ntokens = len(corpus.dictionary)
hidden = model.init_hidden(1)
input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
print("starting with the token <eol>: ")
print(corpus.dictionary.word2idx['<eol>'])
input.fill_(corpus.dictionary.word2idx['<eol>'])
input_histories.add(input.data.clone())

# create FSA
sonnetFSA = fsa.SonnetFSA(readCMU.CMUDict("../data/cmudict.txt"))

# some other inits
blank_flag = False
end_flag = False

# main loop
with open('generated_2.txt', 'w') as outf:
    with open('options.txt', 'w') as tmpf:
        with torch.no_grad():  # no tracking history
            for i in range(args.words):
                print("\n\n\n")
                print("at the " + str(i) + "th iteration.")
                output, hidden = model(input, hidden)
                word_weights = output.squeeze().div(args.temperature).exp().cpu()
                words_idx = torch.multinomial(word_weights, 100)

                # input.fill_(words_idx[0])
                # print(words_idx[0])
                # input_histories.add(input.data.clone())

                words_tmp = []
                for j in range(0, 10):
                    words_tmp.append(corpus.dictionary.idx2word[words_idx[j]])
                tmpf.write(str(words_tmp) + '\n')

                words_idx_list = words_idx.tolist()
                first = words_idx_list[0]
                if blank_flag:
                    print("blank flag entered")
                    if corpus.dictionary.idx2word[first] != '<eol>':
                        print("skipping next word")
                        print(corpus.dictionary.idx2word[first])
                        input.fill_(first)
                        input_histories.add(input.data.clone())
                    elif corpus.dictionary.idx2word[first] == '<eol>':
                        print("seeing an eol, back to writing")
                        input.fill_(first)
                        input_histories.add(input.data.clone())
                        blank_flag = False
                else:
                    for k in range(0, len(words_idx_list)):
                        # print("at k = " + str(k))
                        word = corpus.dictionary.idx2word[words_idx_list[k]]
                        if word == '<eos>' or word == '<blank>' or word == '<eol>':
                            print("RNN think it should end but FSA want to keep going")
                            pass
                        else:
                            FSA_decision = sonnetFSA.accepts(word)
                            # case the word accepted
                            if FSA_decision == 0:
                                # print("accepted: " + word)
                                outf.write(word + ' ')
                                input.fill_(corpus.dictionary.word2idx[word])
                                input_histories.add(input.data.clone())
                                break
                            # case the word not accepted
                            elif FSA_decision == 1:
                                pass
                                # print("declined: " + word)
                            elif FSA_decision == 2:
                                print("accepted: " + word + " and next line")
                                outf.write(word + '\n')
                                input.fill_(corpus.dictionary.word2idx[word])
                                input_histories.add(input.data.clone())
                                blank_flag = True
                                break
                            elif FSA_decision == 3:
                                end_flag = True
                                break
                if end_flag:
                    break

                # if i % args.log_interval == 0:
                    # print('currently at ' + str(i) + 'th iteration.')
                    # input_histories.print()
                # print('| Generated {}/{} words'.format(i, args.words))

print("DONE")
