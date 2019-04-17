import math, random

################################################################################
# Part 0: Utility Functions
################################################################################

def start_pad(n):
    ''' Returns a padding string of length n to append to the front of text
        as a pre-processing step to building n-grams '''
    return '~' * n

def ngrams(n, text):
    ''' Returns the ngrams of the text as tuples where the first element is
        the length-n context and the second is the character '''
    padded = start_pad(n) + text
    ngrams = [tuple((padded[i:n+i],c)) for i,c in enumerate(text)]

    return ngrams

def create_ngram_model(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        model.update(f.read())
    return model

def create_ngram_model_lines(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            model.update(line.strip())
    return model

################################################################################
# Part 1: Basic N-Gram Model
################################################################################

class NgramModel(object):
    ''' A basic n-gram model using add-k smoothing '''

    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.vocab = set()
        self.ngram_probs = {}

    def get_vocab(self):
        ''' Returns the set of characters in the vocab '''
        return self.vocab

    def update(self, text):
        ''' Updates the model n-grams based on text '''
        probs = self.ngram_probs
        grams = ngrams(self.n, text)
        for context, char in grams:
            self.vocab.add(char)
            if context in probs:
                if char in probs[context]:
                    probs[context][char] += 1
                else:
                    probs[context][char] = 1
            else:
                probs[context] = {}
                probs[context][char] = 1

    def prob(self, context, char):
        ''' Returns the probability of char appearing after context '''
        probs = self.ngram_probs
        if context not in probs:
            return 1 / len(self.vocab)
        else:
            total = sum(probs[context].values()) + self.k * len(self.vocab)
            return (probs[context].get(char, 0) + self.k) / total

    def random_char(self, context):
        ''' Returns a random character based on the given context and the
            n-grams learned by this model '''
        r = random.random()
        vocab = sorted(self.vocab)
        prob_sum = 0
        for v in vocab:
            prob_sum += self.prob(context, v)
            if prob_sum > r:
                return v

    def random_text(self, length):
        ''' Returns text of the specified character length based on the
            n-grams learned by this model '''
        context = '~' * self.n
        text = ''
        for _ in range(length):
            char = self.random_char(context)
            text += char
            context = context[1:] + char if self.n > 0 else ''
        return text

    def perplexity(self, text):
        ''' Returns the perplexity of text based on the n-grams learned by
            this model '''
        N = len(text)
        log_sum = 0
        context = '~' * self.n
        for i in range(N):
        	prob = self.prob(context, text[i])
        	if (prob == 0):
        		return float('inf')
        	log_sum += math.log(prob)

        	context = context[1:] + text[i]

        return math.exp((-1/N) * log_sum)

    def is_iambic_pentameter(self, text):
        ''' Returns if given text is iambic pentameter '''
        return (random.random() < 0.5)

################################################################################
# Part 2: N-Gram Model with Interpolation
################################################################################

class NgramModelWithInterpolation(NgramModel):
    ''' An n-gram model with interpolation '''

    def __init__(self, n, k):
        NgramModel.__init__(self, n, k)
        self.lambdas = [1 / (n + 1)] * (n + 1)

    def get_vocab(self):
        return self.vocab

    def update(self, text):
        probs = self.ngram_probs
        grams = ngrams(self.n, text)
        for context, char in grams:
            self.vocab.add(char)
            for i in range(self.n + 1):
                sub_context = context[i:]
                if sub_context in probs:
                    if char in probs[sub_context]:
                        probs[sub_context][char] += 1
                    else:
                        probs[sub_context][char] = 1
                else:
                    probs[sub_context] = {}
                    probs[sub_context][char] = 1

    def prob(self, context, char):
        probs = self.ngram_probs
        prob_calcs = []
        for i in range(self.n + 1):
            sub_context = context[i:]
            if sub_context not in probs:
                prob_calcs.append(1 / len(self.vocab))
            else:
                total = sum(probs[sub_context].values()) + self.k * len(self.vocab)
                prob_calcs.append((probs[sub_context].get(char, 0) + self.k) / total)
        return sum([l * prob for l, prob in zip(self.lambdas, prob_calcs)])

    # TODO
    def set_lambdas(self, lambdas):
        self.lambdas = lambdas

################################################################################
# MAIN
################################################################################

if __name__ == '__main__':
    m = create_ngram_model(NgramModel, 'poems.txt', 4)
    print(m.random_text(200))
	#     print(m.perplexity(f.read()))