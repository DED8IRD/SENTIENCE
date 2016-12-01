"""
ngram_generator_py.py

Generates dictionary containing (2<k<=n)-gram distributions for post files
in the current directory.
Python 2.7 compatible.
"""

# from __future__ import unicode_literals
import nltk, os, time, json, re, io
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
        print ('finish gen ' +str(k)+ ' grams at ' \
                + str(time.time()-start_time))

    # Store clause starts in ngrams[STARTS]
    ngrams['STARTS'] = starts
    start_time = time.time()
    print ('DUMPING JSON...')
    json.dump(ngrams, open(filename, 'wb'))
    print ('DUMPED ' + str(time.time()-start_time) + ' sec')

def getStarts(post_content):
    return re.findall(r'(?:^|(?:[.!?]\s))(\w+)', post_content)

if __name__ == '__main__':

    dataset_dict = {}

    # iterate through all the files in the current directory
    for filename in os.listdir("."):
        if filename == 'post_compilation':
            with io.open(filename, 'r', encoding='utf-8', \
                errors='replace') as corpus:
                    dataset_dict[filename] = corpus.read()

    for filename, infile in dataset_dict.items():
        filename = filename + ".json"
        words = nltk.word_tokenize(infile)
        starts = getStarts(infile)
        ngrams = makeNgrams(filename, words, starts, 8)
        


