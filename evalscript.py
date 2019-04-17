import math, sys, ngram

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python evalscript.py [n for ngram] [perplexity input file]")
    ngram_n = int(sys.argv[1])
    perp_input_file = sys.argv[2]
    m = ngram.create_ngram_model(ngram.NgramModel, 'data/poems.txt', ngram_n)
    with open(perp_input_file, 'r') as fin:
        perp_test_poem = fin.read()
        print(m.perplexity(perp_test_poem))

if __name__ == "__main__":
    main()
