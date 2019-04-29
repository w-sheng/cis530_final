# Literature Review

## Works Cited

Marjan Ghazvininejad, Xing Shi, Yejin Choi, and Kevin Knight. Generating Topical Poetry. *Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing* (2016), 9 pages.

Erica Greene, Tugba Bodrumlu, and Kevin Knight. Automatic Analysis of Rhythmic Poetry with Applications to Generation and Translation. *Proceedings of the 2010 Conference on Empirical Methods in Natural Language Processing* (2010), 10 pages.

Marjan Ghazvininejad, Xing Shi, Jay Priyadarshi, and Kevin Knight. Hafez: an Interactive Poetry Generation System. *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics-System Demonstrations* (2017), 6 pages.

Hisar Manurung, Graeme Ritchie, and Henry Thompson. Towards A Computational Model Of Poetry Generation. *Division of Informatics, University of Edinburgh* (2000), 10 pages.

## Summaries

### Generating Topical Poetry

The researchers built a program called Hafez, which when given a topic by a user, creates poems about that topic. After being given a topic, Hafez finds words related to the topic using pointwise mutual information and word2vec representation cosine similarity. Next, it uses the CMU pronunciation dictionary to determine which of those words rhyme. The researchers also introduce an algorithm to determine slant rhymes. The rhyme pairs are hashed and randomly selected, then a finite state acceptor (FSA) is used to construct the poem while maintaining the correct syllable count, rhyme pairs, and meter. 

A RNN language model is then used to find semantically correct paths in the FSA and return them. The RNN model uses LSTMs and generates the poem in reverse because the number of suitable words preceding the final rhyme word would be too low otherwise. The researchers also implemented an encoder-decoder sequence-to-sequence model. Hafez's results with the RNN and the encoder-decoder model were checked for plagiarism and graded by 25 human judges; the judges preferred the encoder-decoder model?s results.

### Automatic Analysis of Rhythmic Poetry with Applications to Generation and Translation

The paper investigates analyzing, generating, and translating rhythmic poetry; for the purposes of our project, we focus only on the first two. The researchers analyzed poetry by assigning a syllable-stress pattern to each word in a line given a known meter (i.e. iambic pentameter), using S to indicate unstressed syllables and S* to indicate stressed. Due to difficulties, they extended their model beyond using the CMU pronunciation dictionary to use two finite-state transducers (FST). These initially map each English word to sub-sequences of S/S*, each with probability 1/32, and accept any of four near-iambic-pentameter sequences. The result is a probabilistic mapping for words to syllable-stress patterns. Their results have 94\% of word tokens being assigned the gold-standard syllable-stress pattern.

A weighted FST cascade is used for poetry generation, where given a desired meter and rhyme scheme, the model deterministically generates a string of S*/S symbols. They probabilistically select n=1 to 5 tokens, select a word w realizing the n-token sequence, and recurse until the entire line is constructed. To generates lines of poetry, an initial line is chosen from the FST cascade's best 100,000 lines, and then word probabilities are generated using the previous line. Additionally, the researchers use an additional FST that only accepts strings whose final word rhymes with the previous line's final word. 

### Hafez: an Interactive Poetry Generation System

The paper explained Hafez, a poetry generation system, and provided methods to deal with three common problems in poetry generation. The three problems included having difficulties in evaluating poetry quality, unable to adjust the generated poem, and having slow generation speed. To deal with the problems above, the researchers proposed three solutions. First, build a web interface to gather a large amount cheap online user feedbacks. The feedbacks will update the system. Second, add additional weights during decoding to control the style of generated poem. Third, increase speed by pre-calculation, preloading model parameters, and pruning the vocabulary. 

The system implements style control with 9 features: encourage words, curse words, repetition, alliteration, word length, topical words, monosyllabic words, sentiments, concrete words. The model started with a default style weights. After receiving user feedbacks, the system construct new training data with the differences between word choices and ratings and update style weights. The system improves speed with preloading word2vec model, precalculating rhyme type, and shrinking the size of related words. It also attempted to speed up the RNN decoding step by allocating parts to GPU. 

### Towards A Computational Model of Poetry Generation

The paper discusses the use of Lexicalized Tree Adjoining Grammar (LTAG) to generate poetry. The first issue the paper discusses is how it plans to quantify the quality of the output generated by a model. The authors identify three features that may be of some use: (1) phonetics (e.g., rhyme, meter), (2) linguistics (e.g., word choice), and (3) semantics. The paper then discusses the difficulties in quantifying these features. For example, the authors went with the naive approach of counting occurrences of such features, but this favors odd sentence structures (e.g., sentences in which each word starts with the same letter would get high alliteration scores, but would likely lead to a bad poem).

The authors used LTAGs to repeatedly evaluate sentences in poetry and mutate them to produce new sentences. A Tree Adjoining Grammar uses a meta-data structure called a derivation tree, in which operations that are performed on elementary trees are stored. This allows sentence structures to be adjoined or deleted, while keeping track of the operations performed on the sentence. The two operations implemented in the paper are referred to as semantic realization and semantic paraphrasing.

## Published Baseline
TODO