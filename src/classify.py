import math, random

'''This script will predict if a given line in a poem is in iambic pentameter.

The script takes as input:
- a TRAINING file 
- a DEV file
- a TEST file

'''
def getfeats(line):
    features = []

    return features


################################################################################
# FEATURES
################################################################################



################################################################################
# UTIL
################################################################################
def load(file):
    lines = []
    labels = []
    with open(file, encoding='utf-8', errors='ignore') as f:
        for line in f:
            split = lines.split('\t')
            lines.append(split[0])
            labels.append(split[1][0])
    return lines, labels

################################################################################
# MAIN
################################################################################

if __name__ == '__main__':
    train = sys.argv[1]
    dev = sys.argv[2]
    test = sys.argv[3]

    (train_lines, train_labels) = load(train)
    (dev_lines, dev_labels) = load(dev)
    (test_lines, test_labels) = load(test)

    train_feats = []
    train_labels = []
