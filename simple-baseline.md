Insn: You should upload simple-baseline.py and describe it in simple-baseline.md. Your simple-baseline.md should say what score your evaluation metric gives to the simple baseline for your test set.

## Our Baseline Models

In this project, we attempt two tasks: 
* poetry generation
* meter classification

### Poetry Generation

We are attempting to generate poetry to fit a certain meter and rhyme scheme, so a basic baseline would be an n-gram model that generates text character by character. When fed in a bunch of relevant poems of the same meter, the n-gram model would spit out an example baseline poem.

We hope to expand our model to a word-based model (compared to just a character-based one) and to involve neural networks as well to contrast their performance.

**TODO:** Our simple baseline attained a score/perplexity of ????? when run through our evaluation script.

### Meter Classification

For this milestone, we only focused on classifying whether a line of a poem is in iambic pentameter. Our baseline for this is even more basic than our baseline for the previous task. We randomly output 1 or 0 where 1 means it is in iambic and 0 means it is not. 

**TODO:** Our simple baseline attained an f-score of ????? when run through our evaluation script.
