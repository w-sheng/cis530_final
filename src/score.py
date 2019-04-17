import math, sys, ngram

def compute_perplexity(model, input_file):    
    with open(input_file, 'r') as fin:
        perp_test_poem = fin.read()
        print(model.perplexity(perp_test_poem))

    return

def compute_meter_accuracy(input_file):
	return


if __name__ == "__main__":
	if len(sys.argv) != 3:
        sys.exit("Usage: python evalscript.py [n for ngram] [perplexity input file]")

    ngram_n = int(sys.argv[1])
    perp_input_file = sys.argv[2]
    model = ngram.create_ngram_model(ngram.NgramModel, 'data/poems.txt', ngram_n)
    model.write_poem('data/output.txt')

    compute_perplexity(model, perp_input_file)
    compute_meter_accuracy('data/output.txt')
