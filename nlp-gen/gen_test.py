import nltk, os, time, itertools, pickle
from collections import defaultdict, Counter
from generator import sentGenerator 

if __name__ == '__main__':

    # dataset_dict = {}

    # # iterate through all the files in the current directory
    # for filename in os.listdir("."):
    #     if filename.endswith('.txt'):
    #         dataset_dict[filename] = open(filename, 'rU', encoding='utf-8', errors='ignore').read()

    # for filename, infile in dataset_dict.items():
    #     filename = filename + ".pickle"
    #     words = nltk.word_tokenize(infile)
    #     ngrams = makeNgrams(filename, words, 12)

    start_time = time.time()
    ngrams = pickle.load(open('post_compilation.txt.pickle', 'rb'))
    ngrams_out = open('ngrams', 'w')
    gen_out = open('generated.out', 'a')
    print(ngrams, file=ngrams_out)
    gen = sentGenerator(ngrams)
    print(gen(), file=gen_out)
    print ('finish gen at ', time.time()-start_time)

