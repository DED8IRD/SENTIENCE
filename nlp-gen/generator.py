''' 
generator.py

Generates sentences through predicting the next possible word in sentence
based on the context of its preceding words. The next word selected is based
on conditional frequency distributions of n-grams found in the text, with 
(1<k<n) fallback k-grams.
'''

import nltk, random, itertools, bisect, time
from collections import defaultdict, Counter

TERMINAL_PUNCT = ['.', '!', '?', '\n\n']
SPLIT_PUNCT = [',', ';']
CLAUSE_TERMINALS = TERMINAL_PUNCT + SPLIT_PUNCT
STOPWORDS = nltk.corpus.stopwords.words('english')
n = 5

class sentGenerator(object):

    def __init__(self, ngrams, *args, **kwargs):
        if isinstance(ngrams, dict):
            self.ngrams = ngrams
    
    def __call__(self, repetition=7, seed='The'): 
        sentlen = 7
        return self.__generateSentences(self.ngrams, n, sentlen,
                                         repetition, seed)

    def __makeNgrams(self, n):
        """
        Generate n-grams from corpus
        Returns a dictionary of k-grams (from 2 to nth degree)
        """
        start_time = time.time()
        ngrams = dict()
        itergrams = dict()

        for k in range(2,n+1):
            itergrams[k] = list(nltk.ngrams(self.words, k))

        for k, grams in itergrams.items():
            kgrams = defaultdict(Counter)
            for gram in grams:                
                kgram = list(gram)
                key = ' '.join(kgram[:k-1])
                kgrams[key].update({kgram[-1]})
            ngrams[k] = kgrams
            print ('finish gen ', k, 'grams at ', time.time()-start_time)
        return ngrams

    # Generates sentences using a n degree Markov model
    def __markovGen(self, ngrams, n, length, start):
        """
        Param:
            ngrams : dict
                Dictionary of n-grams
                Each key is a word in the corpus
                Each value are possible n-grams with the starting word

            length : int
                Sentence length

            start : string
                Starting word for the generated sentence
                Randomly chosen if not specified
        """
        sent = [start]
        prev = start
        for i in range(length):
            k = len(sent)+1 if len(sent)+1 < n else n
            while not ngrams[k][prev] and k > 2:
                k -= 1
            prev = ' '.join(sent[-k+1:])

            weightedChoices = [(candidate, weight) for (candidate, weight) 
                                in ngrams[k][prev].most_common(20)]
            
            # Choose next candidate word based on a cumulative weight distribution
            choices, weights = zip(*weightedChoices)
            cumdist = list(itertools.accumulate(weights))
            choice = random.random() * cumdist[-1]
            next = choices[bisect.bisect(cumdist, choice)]
            sent.append(next)
            # if sent[-1] in CLAUSE_TERMINALS:
            #     sent.append('')
            #     break
            
        ret = ' '.join(sent)
        cleanPunct = CLAUSE_TERMINALS + ['\'','n\'t',':',')']
        for punct in cleanPunct:
            ret = ret.replace(' %s' % punct, punct)
        ret = ret.replace('%s ' % '(', '(')
        return ret

    def __generateSentences(self, ngrams, n, length, repetition, seed):
        """
        Generates numSent number of sentences.
        """
        randInt = random.randint(1, repetition)
        sent = ''
        for i in range(randInt):
            sent += self.__markovGen(self.ngrams, n, length, seed)
            sent += ' '
        return sent

