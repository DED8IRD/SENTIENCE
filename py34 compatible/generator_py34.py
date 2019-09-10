''' 
generator.py

Generates sentences through predicting the next possible word in sentence
based on the context of its preceding words. The next word selected is based
on conditional frequency distributions of n-grams found in the text, with 
(1<k<n) fallback k-grams.
'''

import nltk, random, itertools, bisect, time
from collections import defaultdict, Counter

CLAUSE_TERMINALS = ['.', '!', '?', '\n\n']
CLAUSE_STARTS = ['The']
STOPWORDS = nltk.corpus.stopwords.words('english')
n = 8

class sentGenerator(object):

    def __init__(self, ngrams, *args, **kwargs):
        if isinstance(ngrams, dict):
            self.ngrams = ngrams
            CLAUSE_STARTS.extend(ngrams['STARTS'])
    
    def __call__(self, seed=None): 
        sentlen = random.randint(7,25)
        repetition = random.randint(1,4)
        if not seed:
            seed = random.choice(CLAUSE_STARTS)
        return self.__generateSentences(self.ngrams, n, sentlen,
                                         repetition, seed)

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
            cum_weight = list(itertools.accumulate(weights))
            choice = random.random() * cum_weight[-1]
            next = choices[bisect.bisect(cum_weight, choice)]
            sent.append(next)

            # End sentences at clause terminals
            if sent[-1] in CLAUSE_TERMINALS:
                sent.append('')
                break
            
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

