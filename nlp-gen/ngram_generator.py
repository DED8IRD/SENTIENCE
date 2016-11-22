"""
ngram_generator.py

Generates dictionary containing (2<k<=n)-gram distributions for post files in the current directory.
"""

import nltk, os, time, itertools, pickle, re
from collections import defaultdict, Counter

def makeNgrams(filename, words, starts, n):
    """
    Generate n-grams from corpus
    Returns a dictionary of k-grams (from 2 to nth degree)
    """
    start_time = time.time()
    ngrams = dict()
    itergrams = dict()

    for k in range(2,n+1):
        itergrams[k] = list(nltk.ngrams(words, k))

    for k, grams in itergrams.items():
        kgrams = defaultdict(Counter)
        for gram in grams:                
            kgram = list(gram)
            key = ' '.join(kgram[:k-1])
            kgrams[key].update({kgram[-1]})
        ngrams[k] = kgrams
        print ('finish gen ', k, 'grams at ', time.time()-start_time)

    # Store clause starts in ngrams[STARTS]
    ngrams['STARTS'] = starts

    pickle.dump(ngrams, open(filename, 'wb'))

def getStarts(post_content):
    return re.findall(r'(?:^|(?:[.!?]\s))(\w+)', post_content)

if __name__ == '__main__':

    dataset_dict = {}

    # iterate through all the files in the current directory
    for filename in os.listdir("."):
        if filename.endswith('.txt'):
            dataset_dict[filename] = open(filename, 'rU', encoding='utf-8', errors='ignore').read()

    for filename, infile in dataset_dict.items():
        filename = filename + ".pickle"
        words = nltk.word_tokenize(infile)
        starts = getStarts(infile)
        ngrams = makeNgrams(filename, words, starts, 8)
        


