

import argparse
import torch
import RNN.utility

parser = argparse.ArgumentParser(description='PyTorch sonnets Language Model')

# Model parameters.
parser.add_argument('--data', type=str, default='./data/sonnets',
                    help='location of the data corpus')
parser.add_argument('--checkpoint', type=str, default='./model.pt',
                    help='model checkpoint to use')
parser.add_argument('--outf', type=str, default='generated.txt',
                    help='output file for generated text')
parser.add_argument('--words', type=int, default='95',
                    help='number of words to generate')
parser.add_argument('--seed', type=int, default=44,
                    help='random seed')
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--temperature', type=float, default=1.0,
                    help='temperature - higher will increase diversity')
parser.add_argument('--log-interval', type=int, default=100,
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

corpus = RNN.utility.Corpus(args.data)
ntokens = len(corpus.dictionary)
hidden = model.init_hidden(1)
input_histories = RNN.utility.input_dict(5)
input = torch.randint(ntokens, (1, 1), dtype=torch.long).to(device)
input_histories.add(input.data.clone())

with open(args.outf, 'w') as outf:
    with open('options.txt', 'w') as tmpf:
        with torch.no_grad():  # no tracking history
            for i in range(args.words):
                output, hidden = model(input, hidden)
                word_weights = output.squeeze().div(args.temperature).exp().cpu()
                words_idx = torch.multinomial(word_weights, 10)
                input.fill_(words_idx[0])
                input_histories.add(input.data.clone())
                words_tmp = []

                for idx in words_idx:
                    words_tmp.append(corpus.dictionary.idx2word[idx])
                tmpf.write(str(words_tmp) + '\n')
                outf.write(words_tmp[0] + ('\n' if i % 20 == 19 else ' '))

                if i % args.log_interval == 0:
                    input_histories.print()
                    print('| Generated {}/{} words'.format(i, args.words))

print('DONE')
