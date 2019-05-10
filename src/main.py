import argparse
import time
import math
import os
import torch
import pprint
import torch.nn as nn
import torch.onnx
import utility
import rnn_model


##############################################################################################
# parser
##############################################################################################

# python main
pp = pprint.PrettyPrinter()
parser = argparse.ArgumentParser()
parser.add_argument('--cuda', action='store_true',
                    help='use CUDA')
parser.add_argument('--data', type=str, default='../data',
                    help='location of the data corpus')
parser.add_argument('--batch_size', type=int, default=60,
                    help='batch size')
parser.add_argument('--bptt', type=int, default=30,
                    help='sequence length')
parser.add_argument('--emsize', type=int, default=200,
                    help='size of word embeddings')
parser.add_argument('--nhid', type=int, default=200,
                    help='number of hidden units per layer')
parser.add_argument('--nlayers', type=int, default=2,
                    help='number of layers')
parser.add_argument('--lr', type=float, default=20,
                    help='initial learning rate')
parser.add_argument('--clip', type=float, default=0.25,
                    help='gradient clipping')
parser.add_argument('--epochs', type=int, default=80,
                    help='upper epoch limit')
parser.add_argument('--log-interval', type=int, default=100, metavar='N',
                    help='report interval')
parser.add_argument('--dropout', type=float, default=0.3,
                    help='dropout applied to layers (0 = no dropout)')
parser.add_argument('--save', type=str, default='model.pt',
                    help='path to save the final model')
parser.add_argument('--onnx-export', type=str, default='',
                    help='path to export the final model in onnx format')

args = parser.parse_args()

##############################################################################################
# main
##############################################################################################

# group words into batches
def batchify(data, bsz, device):
    # Work out how cleanly we can divide the dataset into bsz parts.
    nbatch = data.size(0) // bsz
    # Trim off any extra elements that wouldn't cleanly fit (remainders).
    data = data.narrow(0, 0, nbatch * bsz)
    # Evenly divide the data across the bsz batches.
    data = data.view(bsz, -1).t().contiguous()
    return data.to(device)

# Wraps hidden states in new Tensors, to detach them from their history
def repackage_hidden(h):
    if isinstance(h, torch.Tensor):
        return h.detach()
    else:
        return tuple(repackage_hidden(v) for v in h)

# turn batch into sequences
# get_batch subdivides the source data into chunks of length args.bptt.
# If source is equal to the example output of the batchify function, with
# a bptt-limit of 2, we'd get the following two Variables for i = 0:
# ┌ a g m s ┐ ┌ b h n t ┐
# └ b h n t ┘ └ c i o u ┘
# Note that despite the name of the function, the subdivison of data is not
# done along the batch dimension (i.e. dimension 1), since that was handled
# by the batchify function. The chunks are along dimension 0, corresponding
# to the seq_len dimension in the LSTM.
def get_batch(source, i):
    seq_len = min(args.bptt, len(source) - 1 - i)
    data = source[i:i+seq_len]
    target = source[i+1:i+1+seq_len].view(-1)
    return data, target

# eval the loss
def evaluate(data_source, model, corpus, criterion, ebs):
    # Turn on evaluation mode which disables dropout.
    model.eval()
    total_loss = 0.
    ntokens = len(corpus.dictionary)
    hidden = model.init_hidden(ebs)
    with torch.no_grad():
        for i in range(0, data_source.size(0) - 1, args.bptt):
            data, targets = get_batch(data_source, i)
            output, hidden = model(data, hidden)
            output_flat = output.view(-1, ntokens)
            total_loss += len(data) * criterion(output_flat, targets).item()
            hidden = repackage_hidden(hidden)
    return total_loss / (len(data_source) - 1)


def train(model, corpus, train_data, criterion, lr, epoch):
    # Turn on training mode which enables dropout.
    model.train()
    total_loss = 0.
    start_time = time.time()
    ntokens = len(corpus.dictionary)
    hidden = model.init_hidden(args.batch_size)
    for batch, i in enumerate(range(0, train_data.size(0) - 1, args.bptt)):
        # standard training process
        # print(len(train_data))
        # print(i)
        data, targets = get_batch(train_data, i)
        # print(data)
        # print(targets)
        # print("\n\n")
        hidden = repackage_hidden(hidden)
        model.zero_grad()
        output, hidden = model(data, hidden)
        loss = criterion(output.view(-1, ntokens), targets)
        loss.backward()
        # prevent exploding gradient
        torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)
        for p in model.parameters():
            p.data.add_(-lr, p.grad.data)
        total_loss += loss.item()
        # print training loss
        if batch % args.log_interval == 0 and batch > 0:
            cur_loss = total_loss / args.log_interval
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:5d}/{:5d} batches | lr {:02.2f} | ms/batch {:5.2f} | '
                    'loss {:5.2f} | ppl {:8.2f}'.format(
                epoch, batch, len(train_data) // args.bptt, lr,
                elapsed * 1000 / args.log_interval, cur_loss, math.exp(cur_loss)))
            total_loss = 0
            start_time = time.time()


def export_onnx(path, model, device, batch_size, seq_len):
    print('The model is also exported in ONNX format at {}'.
          format(os.path.realpath(args.onnx_export)))
    model.eval()
    dummy_input = torch.LongTensor(seq_len * batch_size).zero_().view(-1, batch_size).to(device)
    hidden = model.init_hidden(batch_size)
    torch.onnx.export(model, (dummy_input, hidden), path)

##############################################################################################
# main
##############################################################################################

def main(args):
    # setup GPU version
    if torch.cuda.is_available():
        if not args.cuda:
            print("WARNING: You have a CUDA device, so you should probably run with --cuda")
    device = torch.device("cuda" if args.cuda else "cpu")

    # obtain corpus
    corpus = utility.Corpus(args.data, "nopadding")
    # print(len(corpus.train.data.numpy()))
    # print(corpus.train.data.numpy()[0:100])
    # print(corpus.dictionary.word2idx['<eos>'])
    print("corpus set")
    print(corpus.flag)

    # split into batches
    eval_batch_size = 10
    train_data = batchify(corpus.train, args.batch_size, device)
    # print(len(train_data.data.numpy()))
    val_data = batchify(corpus.valid, eval_batch_size, device)
    test_data = batchify(corpus.test, eval_batch_size, device)

    # init model
    ntokens = len(corpus.dictionary)
    model = rnn_model.RNNModel(ntokens, args.emsize, args.nhid, args.nlayers, args.dropout).to(device)
    criterion = nn.CrossEntropyLoss()

    # loop for epoch
    best_val_loss = None
    lr = args.lr
    print("entering the training loop")
    for epoch in range(1, args.epochs + 1):
        print(1)
        epoch_start_time = time.time()
        print(2)
        train(model, corpus, train_data, criterion, lr, epoch)
        print(3)
        val_loss = evaluate(val_data, model, corpus, criterion, eval_batch_size)
        print(4)
        print('-' * 89)
        print('| end of epoch {:3d} | time: {:5.2f}s | valid loss {:5.2f} | '
              'valid ppl {:8.2f}'.format(epoch, (time.time() - epoch_start_time),
                                         val_loss, math.exp(val_loss)))
        print('-' * 89)
        if not best_val_loss or val_loss < best_val_loss:
            with open(args.save, 'wb') as f:
                torch.save(model, f)
            best_val_loss = val_loss
        else:
            lr *= 3.0/4.0

    with open(args.save, 'rb') as f:
        model = torch.load(f)
        model.rnn.flatten_parameters()

    # Run on test data.
    test_loss = evaluate(test_data, model, corpus, criterion, eval_batch_size)
    print('=' * 89)
    print('| End of training | test loss {:5.2f} | test ppl {:8.2f}'.format(
        test_loss, math.exp(test_loss)))
    print('=' * 89)

    if len(args.onnx_export) > 0:
        export_onnx(args.onnx_export, device, model, batch_size=1, seq_len=args.bptt)

##############################################################################################
# main
##############################################################################################

if __name__ == '__main__':
    args = parser.parse_args()
    pp.pprint(args)
    main(args)
