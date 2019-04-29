import math, sys, simple_baseline, readCMU
from nltk.tokenize import word_tokenize

################################################################################
# Computing Perplexity of Generated Poetry
################################################################################
def compute_perplexity(model, input):    
    with open(input, 'r') as fin:
        perp_test_poem = fin.read()
        print('Perplexity:')
        print(model.perplexity(perp_test_poem))

################################################################################
# Computing Classification of Iambic Pentameter
################################################################################
## Calculates the precision of the predicted labels
def get_precision(y_pred, y_true):
    num_pred = len(y_pred)
    num_correct = 0

    for y1, y2 in zip(y_pred, y_true):
        if y1 == y2:
            num_correct += 1

    precision = num_correct / num_pred 

    return precision
    
## Calculates the recall of the predicted labels
def get_recall(y_pred, y_true):
    num_true = y_true.count(1)
    num_selected = 0

    for y1, y2 in zip(y_pred, y_true):
        if y1 == y2 == 1:
            num_selected += 1

    recall = num_selected / num_true 
    
    return recall

## Calculates the f-score of the predicted labels
def get_fscore(y_pred, y_true):
    precision = get_precision(y_pred, y_true)
    recall = get_recall(y_pred, y_true)
    fscore = 2 * precision * recall / (precision + recall)

    return fscore

# gold = list of 0's and 1's which indicate the target meter; for the time being this is ignored and we use the iambic array instead
# this function is broken because word rhythem depends on the context
def compute_meter_accuracy(model, lines, gold, CMUdict):
    pred = []
    for l in lines:
        index = 0
        words = [word.lower() for word in word_tokenize(l) if word.isalpha()]
        is_iambic = True
        # check if this line is in iambic pentameter, 1 if yes else 0
        for word in words:
            word_stress = CMUdict.get_stresses(word)
            if len(word_stress) == 0:
                print(word + " is not in dictionary")
                pred.append(0)
                is_iambic = False
                break
            if index + len(word_stress) > len(gold):
                pred.append(0)
                print('too big' + words)
                is_iambic = False
                break
            if word_stress == gold[index:index + len(word_stress)]:
                index += len(word_stress)
            else:
                pred.append(0)
                print(word + ' makes it not iambic')
                is_iambic = False
                break
        if is_iambic:
            pred.append(1)

    print(pred)
    print('\nF-Score:')
    print(get_fscore(pred, gold))

################################################################################
# Loading Files
################################################################################
def load_file(input):
    lines = []
    labels = []   
    with open(input, 'rt', encoding="utf8") as f:
        for line in f:
            line_split = line.split("\t")
            if len(line_split) > 1:
                lines.append(line_split[0])
                labels.append(int(line_split[1]))

    return lines, labels

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: python src/score.py [n for ngram] [training input file] [perplexity input file] [classification input file]")

    ngram_n = int(sys.argv[1])
    training_input_file = sys.argv[2]
    perp_input_file = sys.argv[3]
    class_input_file = sys.argv[4]

    (class_lines, class_gold) = load_file(class_input_file)

    model = simple_baseline.create_ngram_model(simple_baseline.NgramModel, training_input_file, ngram_n)
    # model.write_poem('data/output.txt')

    compute_perplexity(model, perp_input_file)
    iambic = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1] * 14
    with open("../data/meter_accuracy_test_sonnet.txt", 'r') as f:
        single_iambic_sonnet = [line.strip() for line in f]
    compute_meter_accuracy(model, single_iambic_sonnet, iambic, readCMU.CMUDict("../data/cmudict.txt"))
