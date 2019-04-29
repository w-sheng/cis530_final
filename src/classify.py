import math, pickle, random, sys
from readCMU import CMUDict
from score import get_fscore
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import LinearSVC

'''This script will predict if a given line in a poem is in iambic pentameter.

The script takes as input:
- a TRAINING file 
- a DEV file
- a TEST file

'''
def get_feats(line, cmu_dict):
    features = []
    features.append(('line',line))
    features.append(('num_words',num_words(line)))
    features.append(('num_chars',num_chars(line)))
    features.append(('stress_seq',stress_seq(line, cmu_dict)))
    features.append(('num_syllables',num_syllables(line, cmu_dict)))

    return dict(features)


################################################################################
# FEATURES
################################################################################

def num_words(line):
    return line.count(' ') + 1

def num_chars(line):
    return len(line)

def stress_seq(line, cmu_dict):
    words = line.split(' ')
    seq = ''
    for w in words:
        seq += ''.join([str(s) for s in cmu_dict.get_stresses(w)])
    return seq

def num_syllables(line, cmu_dict):
    words = line.split(' ')
    count = 0
    for w in words:
        count += len(cmu_dict.get_stresses(w))
    return count

################################################################################
# UTIL
################################################################################
def load(file):
    lines = []
    labels = []
    with open(file, encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line != '\n':
                split = line.split('\t')
                lines.append(split[0])
                labels.append(int(str(split[1])[0]))
    return lines, labels

################################################################################
# MAIN
################################################################################

if __name__ == '__main__':
    train = sys.argv[1]
    dev = sys.argv[2]
    test = sys.argv[3]

    cmu_dict = CMUDict("../data/cmudict.txt")

    (train_lines, train_labels) = load(train)
    (dev_lines, dev_labels) = load(dev)
    (test_lines, test_labels) = load(test)

    print(train_labels)
    print(dev_labels)
    print(test_labels)

    train_feats = []
    dev_feats = []
    test_feats = []

    for l in train_lines:
        train_feats.append(get_feats(l,cmu_dict))
    for l in dev_lines:
        dev_feats.append(get_feats(l,cmu_dict))
    for l in test_lines:
        test_feats.append(get_feats(l,cmu_dict))

    vectorizer = DictVectorizer()

    # Training
    X_train = vectorizer.fit_transform(train_feats)
    # model = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    # model = SGDClassifier(max_iter=1000, tol=1e-3)
    # model = Perceptron(verbose=1)
    # model = LinearSVC(random_state=0, tol=1e-5)
    model = AdaBoostClassifier(n_estimators=100)
    model.fit(X_train, train_labels)
    pickle.dump(model, open('../classification_models/ada_boost_model', 'wb'))
    # model = pickle.load(open('model', 'rb'))

    # Dev
    X_dev = vectorizer.transform(dev_feats)
    y_dev = model.predict(X_dev)
    fscore_dev = get_fscore(y_dev,dev_labels)

    print('Dev F-Score:')
    print(fscore_dev)
    print(y_dev)

    # Testing
    X_test = vectorizer.transform(test_feats)
    y_test = model.predict(X_test)
    fscore_test = get_fscore(y_test,test_labels)

    print('Test F-Score:')
    print(fscore_test)
    print(y_test)
