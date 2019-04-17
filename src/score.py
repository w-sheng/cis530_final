import math, sys, simple_baseline

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

def compute_meter_accuracy(model, lines, gold):
    pred = []
    for l in lines:
        pred.append(model.is_iambic_pentameter(l))

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
            lines.append(line_split[0].lower())
            labels.append(int(line_split[1]))

    return lines, labels

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: python score.py [n for ngram] [training input file] \
            [perplexity input file] [classification input file]")

    ngram_n = int(sys.argv[1])
    training_input_file = sys.argv[2]
    perp_input_file = sys.argv[3]
    class_input_file = sys.argv[4]

    model = simple_baseline.create_ngram_model(simple_baseline.NgramModel, training_input_file, ngram_n)
    model.write_poem('data/output.txt')
    (class_lines, class_gold) = load_file(class_input_file)

    compute_perplexity(model, perp_input_file)
    compute_meter_accuracy(model, class_lines, class_gold)
