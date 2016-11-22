import nltk, os, time, itertools, pickle, re, random
from collections import defaultdict, Counter
from generator import sentGenerator 

if __name__ == '__main__':

    start_time = time.time()
    ngrams = pickle.load(open('post_compilation.txt.pickle', 'rb'))
    gen_out = open('generated.out', 'a')
    gen = sentGenerator(ngrams)
    print(gen(), file=gen_out)
    print ('finish gen at ', time.time()-start_time)

